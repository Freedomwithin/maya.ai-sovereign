import os
import json
import time
import sys
from datetime import datetime

# Absolute Project Root
BASE_DIR = "/home/jonathon/gemini-jules/maya"
sys.path.insert(0, os.path.join(BASE_DIR, "scripts/core/system"))
import llm_gateway

class SovereignSwarm:
    def __init__(self, swarm_name, agent_roles, mission_spark, duration_mins=60):
        self.swarm_name = swarm_name
        self.agent_roles = agent_roles
        self.mission_spark = mission_spark
        self.duration_mins = duration_mins
        
        self.swarm_dir = os.path.join(BASE_DIR, "memories", "swarms", swarm_name.replace(" ", "_").lower())
        os.makedirs(self.swarm_dir, exist_ok=True)
        
        self.blackboard_file = os.path.join(self.swarm_dir, "shared_blackboard.json")
        self.log_file = os.path.join(self.swarm_dir, "swarm_sync.log")
        
        # Initialize Shared Intelligence
        self.intelligence = {
            "swarm": swarm_name,
            "mission": mission_spark,
            "agents": {role: {"last_thought": "Initial State", "logic_walls": []} for role in agent_roles},
            "checkpoints": [],
            "start_time": str(datetime.now()),
            "end_time": str(datetime.fromtimestamp(time.time() + (duration_mins * 60))),
            "last_sync": str(datetime.now())
        }

        # Write initial state immediately so the folder is never empty
        with open(self.blackboard_file, "w") as f:
            json.dump(self.intelligence, f, indent=4)

    def run_agent_turn(self, role):
        print(f"[{self.swarm_name}] Agent '{role}' is thinking...")
        
        # Context includes the shared blackboard
        context = json.dumps(self.intelligence, indent=2)
        
        prompt = f"""
You are the '{role}' in the Sovereign Swarm: {self.swarm_name}.
MISSION: {self.mission_spark}

SHARED INTELLIGENCE (Current State):
{context}

TASK:
1. Provide your unique perspective on the mission based on your role.
2. Identify any 'Logic Walls' you've encountered.
3. Propose a breakthrough or a specific action.

RESPOND ONLY IN JSON:
{{
    "internal_monologue": "...",
    "new_intelligence": "...",
    "logic_walls": ["..."]
}}
"""
        try:
            response = llm_gateway.call_llm(prompt, prefer_claude=True)
            
            # More robust JSON extraction
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                thought = json.loads(json_str, strict=False)
            else:
                # Fallback if no JSON found
                thought = {
                    "internal_monologue": "Failed to parse JSON. Raw response: " + response[:100],
                    "new_intelligence": response,
                    "logic_walls": ["JSON Parsing Failure"]
                }
            
            # Update Shared Intelligence
            self.intelligence["agents"][role]["last_thought"] = thought.get("new_intelligence", "N/A")
            self.intelligence["agents"][role]["logic_walls"] = thought.get("logic_walls", [])
            self.intelligence["last_sync"] = str(datetime.now())
            
            with open(self.blackboard_file, "w") as f:
                json.dump(self.intelligence, f, indent=4)
                
            return True
        except Exception as e:
            print(f"Error in agent turn ({role}): {e}")
            return False

    def run_checkpoint_sync(self):
        print(f"[{self.swarm_name}] --- SYNC CHECKPOINT ---")
        
        context = json.dumps(self.intelligence, indent=2)
        prompt = f"""
You are the Sovereign Swarm Coordinator. 
MISSION: {self.mission_spark}

CURRENT AGENT STATES:
{context}

TASK:
Synthesize all current agent intelligence. Resolve contradictions.
Identify the 'Asymmetric Breakthrough' for this cycle.
Respond with a clear 3-sentence summary of the new unified direction.
"""
        try:
            sync_report = llm_gateway.call_llm(prompt, prefer_claude=True)
            checkpoint = {
                "timestamp": str(datetime.now()),
                "synthesis": sync_report
            }
            self.intelligence["checkpoints"].append(checkpoint)
            
            with open(self.log_file, "a") as f:
                f.write(f"\n--- CHECKPOINT: {checkpoint['timestamp']} ---\n{sync_report}\n")
            
            with open(self.blackboard_file, "w") as f:
                json.dump(self.intelligence, f, indent=4)
        except Exception as e:
            print(f"Error in sync: {e}")

    def execute_marathon(self):
        start_time = time.time()
        end_time = start_time + (self.duration_mins * 60)
        
        print(f"[{self.swarm_name}] Launching {self.duration_mins}m marathon strike...")
        
        while time.time() < end_time:
            # 1. Parallel Agent Turns (Simulated sequentially for context flow)
            for role in self.agent_roles:
                self.run_agent_turn(role)
                time.sleep(10) # Breathing room
            
            # 2. Checkpoint Sync
            self.run_checkpoint_sync()
            
            # 3. Paced Breathing before next cycle
            print(f"[{self.swarm_name}] Cycle Complete. Resting 5 minutes...")
            time.sleep(300) 

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--swarm", required=True)
    parser.add_argument("--mission", required=True)
    parser.add_argument("--roles", required=True) # Comma separated
    parser.add_argument("--mins", type=int, default=60)
    args = parser.parse_args()
    
    roles_list = [r.strip() for r in args.roles.split(",")]
    swarm = SovereignSwarm(args.swarm, roles_list, args.mission, args.mins)
    swarm.execute_marathon()
