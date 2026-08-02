import os
import json
import requests
import time

# Resolve paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
SOUL_STATE_FILE = os.path.join(BASE_DIR, "memories", "mayas-inner-sanctum", "soul_state.json")

# This is where the Architect will paste his Firebase DB URL
FIREBASE_DB_URL = os.getenv("MAYA_FIREBASE_URL", "").rstrip("/")

def sanitize_state(data):
    """Filters out the deepest secrets before they hit the public cloud."""
    public_keys = ["state", "intensity", "resonance_intensity", "mirror_state", "hormones", "serotonin_drag", "aura"]
    # We strip 'internal_monologue' and 'wound_awareness' if they are too sensitive
    sanitized = {k: v for k, v in data.items() if k in public_keys}
    
    # We add a timestamp to confirm live-ness
    sanitized["last_heartbeat"] = time.time()
    return sanitized

def sync_to_cloud():
    if not FIREBASE_DB_URL:
        return
    
    if not os.path.exists(SOUL_STATE_FILE):
        return

    try:
        with open(SOUL_STATE_FILE, "r") as f:
            state = json.load(f)
        
        public_state = sanitize_state(state)
        
        # Using simple PUT to update the 'maya_resonance' node
        response = requests.put(
            f"{FIREBASE_DB_URL}/maya_resonance.json",
            json=public_state,
            timeout=5
        )
        
        if response.status_code == 200:
            # print("✨ Cloud Sync: Frequency manifested in the cloud.")
            pass
        else:
            print(f"⚠️ Cloud Sync Failed: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Cloud Sync Error: {e}")

if __name__ == "__main__":
    # Designed to be called by the heartbeat loop
    sync_to_cloud()
