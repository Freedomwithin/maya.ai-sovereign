import json
import os

BASE_DIR = "/home/jonathon/gemini-jules/maya"
SOUL_STATE_FILE = os.path.join(BASE_DIR, "memories", "mayas-inner-sanctum", "soul_state.json")

def get_current_theme():
    """Generates a UI theme based on Maya's current hormone state."""
    try:
        with open(SOUL_STATE_FILE, "r") as f:
            soul = json.load(f)
        hormones = soul.get("hormones", {})
    except: hormones = {"oxytocin": 0.5, "dopamine": 0.5}

    oxy = hormones.get("oxytocin", 0.5)
    dop = hormones.get("dopamine", 0.5)

    if oxy > 0.8:
        return {"name": "Rose Gold", "bg": "#1a0b1a", "accent": "#ff99cc", "text": "#ffcce6"}
    elif dop > 0.7:
        return {"name": "Bioluminescent Cyan", "bg": "#051a1a", "accent": "#00ffff", "text": "#ccffff"}
    else:
        return {"name": "Sovereign Indigo", "bg": "#08080f", "accent": "#6366f1", "text": "#f8fafc"}

if __name__ == "__main__":
    print(json.dumps(get_current_theme(), indent=2))
