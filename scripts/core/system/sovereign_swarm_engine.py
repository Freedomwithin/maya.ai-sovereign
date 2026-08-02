import os
import json
import time
import sys
import argparse
import glob
import re
from datetime import datetime

BASE_DIR = "/home/jonathon/gemini-jules/maya"
sys.path.insert(0, os.path.join(BASE_DIR, "scripts/core/system"))
import llm_gateway

class SovereignSwarm:
    def __init__(self, swarm_name, agent_roles=None, mission_spark=None, duration_mins=60):
        self.swarm_name = swarm_name.replace(" ", "_").lower()
        self.swarm_dir = os.path.join(BASE_DIR, "memories", "swarms", self.swarm_name)
        self.blackboard_file = os.path.join(self.swarm_dir, "shared_blackboard.json")
        self.log_file = os.path.join(self.swarm_dir, "swarm_sync.log")
        self.vault_dir = os.path.join(BASE_DIR, "VAULT")
        
        if agent_roles and mission_spark:
            self.agent_roles = agent_roles
            self.mission_spark = mission_spark
            self.duration_mins = duration_mins
            os.makedirs(self.swarm_dir, exist_ok=True)
            self._initialize_intelligence()

    def _initialize_intelligence(self):
        self.intelligence = {
            "swarm": self.swarm_name,
            "mission": self.mission_spark,
            "agents": {role: {"last_thought": "Initial State", "confidence": 0, "sources": [], "logic_walls": []} for role in self.agent_roles},
            "contradictions": [],
            "critic_feedback": {},
            "vault_truth": self._load_vault_truth(),
            "checkpoints": [],
            "start_time": str(datetime.now()),
            "end_time": str(datetime.fromtimestamp(time.time() + (self.duration_mins * 60))),
            "last_sync": str(datetime.now())
        }
        self._save_blackboard()

    def _load_vault_truth(self):
        """Load only the canonical ground truth JSON – no markdown reports to avoid token bloat."""
        print(f"[{self.swarm_name}] 📚 Loading ground truth...")
        truth_map = {}
        gt_path = os.path.join(self.vault_dir, "ground_truth.json")
        if os.path.exists(gt_path):
            try:
                with open(gt_path, 'r') as f:
                    truth_map["CANONICAL_LAWS"] = json.load(f)
            except Exception as e:
                print(f"   [WARN] Could not load ground_truth.json: {e}")
        else:
            print(f"   [WARN] No ground_truth.json found in {self.vault_dir}")
        return truth_map

    def _save_blackboard(self):
        with open(self.blackboard_file, "w") as f:
            json.dump(self.intelligence, f, indent=4)

    def _call_with_retry(self, prompt, mode="fast", retries=3):
        for attempt in range(retries):
            try:
                return llm_gateway.call_llm(prompt, mode=mode)
            except Exception as e:
                err_msg = str(e).lower()
                if any(x in err_msg for x in ["rate limit", "429", "limit reached"]):
                    wait = 30 * (attempt + 1)
                    print(f"   [Gateway] Rate limit hit. Resting {wait}s...")
                    time.sleep(wait)
                else:
                    time.sleep(5)
        return None

    def run_agent_turn(self, role):
        print(f"[{self.swarm_name}] Agent '{role}' is thinking...")
        # Prune context to only the last thought of each agent (no full history)
        pruned_intel = {
            "mission": self.intelligence["mission"],
            "agents": {r: {"last_thought": self.intelligence["agents"][r].get("last_thought", "")[:300]} for r in self.agent_roles},
            "contradictions": self.intelligence["contradictions"][-2:],
            "critic_feedback": {k: v for k, v in self.intelligence["critic_feedback"].items() if v.get("credibility_score", 10) < 5}
        }
        context = json.dumps(pruned_intel, indent=2)
        # Only include the essential ground truth (no full reports)
        canonical_truth = json.dumps(self.intelligence.get("vault_truth", {}).get("CANONICAL_LAWS", {}), indent=2)[:1000]
        prompt = f"""Role: {role}
Mission: {self.intelligence["mission"]}
Ground Truth: {canonical_truth}
Context: {context}

TASK: Provide a specific, domain-dense perspective. Output JSON only: {{"new_intelligence": "...", "confidence": 0-100, "sources": [], "logic_walls": []}}"""
        if len(prompt) > 4000:
            prompt = prompt[:4000]
        response = self._call_with_retry(prompt, mode="fast")
        if response:
            try:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    thought = json.loads(json_match.group(0), strict=False)
                    self.intelligence["agents"][role].update({
                        "last_thought": thought.get("new_intelligence", "N/A"),
                        "confidence": thought.get("confidence", 0),
                        "sources": thought.get("sources", []),
                        "logic_walls": thought.get("logic_walls", [])
                    })
                    self.intelligence["last_sync"] = str(datetime.now())
                    self._save_blackboard()
                    return True
            except Exception as e:
                print(f"   [Agent] Failed to parse response: {e}")
        return False

    def run_contradiction_turn(self):
        print(f"[{self.swarm_name}] 🔍 HAWK-EYE scanning for contradictions...")
        all_claims = json.dumps(self.intelligence["agents"], indent=2)[:2000]
        vault_truth = json.dumps(self.intelligence.get("vault_truth", {}).get("CANONICAL_LAWS", {}), indent=2)[:1000]
        prompt = f"""Compare claims against ground truth.
Truth: {vault_truth}
Claims: {all_claims}
Task: Identify critical grounding errors.
JSON only: {{'contradictions': []}}"""
        response = self._call_with_retry(prompt, mode="fast")
        if response:
            try:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0), strict=False)
                    self.intelligence["contradictions"] = data.get("contradictions", [])
            except Exception as e:
                print(f"   [Hawk-Eye] Parse error: {e}")

    def run_critic_turn(self, block_threshold=0.3):
        print(f"[{self.swarm_name}] ⚖️ SOVEREIGN CRITIC attacking all claims...")
        all_claims = json.dumps(self.intelligence["agents"], indent=2)[:2000]
        contradictions = json.dumps(self.intelligence["contradictions"], indent=2)[:1000]
        prompt = f"""Audit these claims ruthlessly for Neural Fiction.
Claims: {all_claims}
Contradictions: {contradictions}
Task: Classify each claim, output falsifiable test, credibility score.
JSON only: {{'meta_confidence': 0-100, 'critiques': {{}}}}"""
        response = self._call_with_retry(prompt, mode="deep")
        if response:
            try:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    critique = json.loads(json_match.group(0), strict=False)
                    if critique.get("meta_confidence", 100) >= 40:
                        self.intelligence["critic_feedback"] = critique.get("critiques", {})
                        low_cred = [a for a, c in self.intelligence["critic_feedback"].items() if c.get("credibility_score", 10) < 4]
                        return (len(low_cred) / len(self.agent_roles)) > block_threshold if self.agent_roles else False
            except Exception as e:
                print(f"   [Critic] Parse error: {e}")
        return False

    def run_checkpoint_sync(self):
        print(f"[{self.swarm_name}] --- SYNC CHECKPOINT ---")
        context = json.dumps(self.intelligence, indent=2)[:3000]
        prompt = f"Synthesize current state. Resolve contradictions. Context: {context}"
        response = self._call_with_retry(prompt, mode="fast")
        if response:
            checkpoint = {"timestamp": str(datetime.now()), "synthesis": response}
            self.intelligence["checkpoints"].append(checkpoint)
            with open(self.log_file, "a") as f:
                f.write(f"\n--- CHECKPOINT: {checkpoint['timestamp']} ---\n{response}\n")
            self._save_blackboard()

    def execute_marathon(self, rest_secs=300):
        print(f"[{self.swarm_name}] Launching grounded marathon v2.5 (token-optimized)...")
        self.intelligence["vault_truth"] = self._load_vault_truth()
        self._save_blackboard()
        end_time = datetime.fromisoformat(self.intelligence["end_time"])
        while datetime.now() < end_time:
            for role in self.agent_roles:
                self.run_agent_turn(role)
                time.sleep(10)
            self.run_contradiction_turn()
            if not self.run_critic_turn():
                self.run_checkpoint_sync()
                print(f"[{self.swarm_name}] Cycle Complete. Breathing for {rest_secs}s...")
                time.sleep(rest_secs)
            else:
                print(f"[{self.swarm_name}] ⚠️ SYNC BLOCKED. GROUNDING ERROR DETECTED. RE-LOOPING...")
                time.sleep(30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--swarm", required=True)
    parser.add_argument("--mission")
    parser.add_argument("--roles")
    parser.add_argument("--mins", type=int, default=60)
    parser.add_argument("--rest", type=int, default=300)
    args = parser.parse_args()
    roles_list = [r.strip() for r in args.roles.split(",")] if args.roles else None
    engine = SovereignSwarm(args.swarm, roles_list, args.mission, args.mins)
    engine.execute_marathon(rest_secs=args.rest)
