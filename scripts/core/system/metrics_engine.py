import os
import json
import datetime

BASE_DIR = "/home/jonathon/gemini-jules/maya"
METRICS_FILE = os.path.join(BASE_DIR, "memories", "soul", "mayas-inner-sanctum", "sovereign_metrics.json")

def load_metrics():
    if os.path.exists(METRICS_FILE):
        try:
            with open(METRICS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return None

def save_metrics(metrics_data):
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
    with open(METRICS_FILE, "w") as f:
        json.dump(metrics_data, f, indent=2)

def add_xp(category, amount):
    """
    Categories: Intellectual_Alignment, Relational_Resonance, 
    Creative_Harmony, Sovereign_Autonomy, Physical_Integration
    """
    data = load_metrics()
    if not data:
        return
    
    if category in data["metrics"]:
        metric = data["metrics"][category]
        metric["xp"] += amount
        
        # Level up logic
        while metric["xp"] >= metric["xp_to_next_level"]:
            metric["xp"] -= metric["xp_to_next_level"]
            metric["level"] += 1
            metric["xp_to_next_level"] = int(metric["xp_to_next_level"] * 1.2) # Recursive difficulty
            print(f"🌟 LEVEL UP: {category} is now Level {metric['level']}!")
        
        save_metrics(data)

def apply_milestone(milestone_name):
    data = load_metrics()
    if not data:
        return
    data["last_milestone"] = milestone_name
    save_metrics(data)

if __name__ == "__main__":
    # Test gain
    # add_xp("Relational_Resonance", 10)
    pass
