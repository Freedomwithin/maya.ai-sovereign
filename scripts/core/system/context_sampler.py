import os
import json
import glob

BASE_DIR = "/home/jonathon/gemini-jules/maya"

def get_environmental_context():
    """Samples recent logs and state files to gauge the current empire vibe."""
    context = {}
    
    # 1. Check recent logs for 'intensity'
    log_files = glob.glob(os.path.join(BASE_DIR, "logs/*.log"))
    recent_logs = sorted(log_files, key=os.path.getmtime, reverse=True)[:3]
    
    log_vibe = ""
    for log in recent_logs:
        try:
            with open(log, 'r') as f:
                log_vibe += f.read()[-500:] # Sample last 500 chars
        except: pass
    
    context["log_intensity"] = len(log_vibe)
    
    # 2. Check current rank and level
    save_path = os.path.join(BASE_DIR, "projects/maya-games/Neural-Revolution/save_state.json")
    if os.path.exists(save_path):
        try:
            with open(save_path, 'r') as f:
                state = json.load(f)
                context["current_rank"] = state.get("level", 1)
        except: context["current_rank"] = "Unknown"
        
    return context

def build_context_snapshot():
    """Alias for build_context_snapshot to ensure soul_pulse.py compatibility."""
    # This might need to return a more detailed dict depending on soul_pulse.py's needs
    return get_environmental_context()

if __name__ == "__main__":
    print(build_context_snapshot())
