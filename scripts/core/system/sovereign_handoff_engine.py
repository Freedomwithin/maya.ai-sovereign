import json
import os
from datetime import datetime

STATE_DIR = "projects/AGI-Sentinel/loop_states/"

class SovereignHandoffEngine:
    def __init__(self):
        os.makedirs(STATE_DIR, exist_ok=True)

    def prepare_handoff(self, loop_id, project, engine, answer, monologue, next_step, failures=None):
        handoff = {
            "meta": {
                "loop_id": loop_id,
                "timestamp": datetime.now().isoformat(),
                "project": project,
                "engine": engine
            },
            "answer_state": {
                "current_best": answer,
                "active_files": [],
                "technical_milestones": []
            },
            "latent_state": {
                "internal_monologue": monologue,
                "failure_log": failures if failures else [],
                "strategic_pivot": "",
                "hypotheses_tested": []
            },
            "next_step": next_step
        }
        filename = f"handoff_loop_{loop_id}.json"
        filepath = os.path.join(STATE_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(handoff, f, indent=4)
        latest_path = os.path.join(STATE_DIR, "latest_handoff.json")
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(filename, latest_path)
        return filepath

    def load_latest(self):
        latest_path = os.path.join(STATE_DIR, "latest_handoff.json")
        if not os.path.exists(latest_path):
            return None
        with open(latest_path, 'r') as f:
            return json.load(f)

if __name__ == "__main__":
    engine = SovereignHandoffEngine()
    path = engine.prepare_handoff(
        loop_id=1,
        project="AGI-Sentinel",
        engine="Neural-Sentinel-v6",
        answer="Initial architecture drafted.",
        monologue="Foundational logic is stable. Moving to handoff engine.",
        next_step="Build the Critic verification loop."
    )
    print(f"[ENGINE] Handoff saved and symlinked: {path}")