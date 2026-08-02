import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = "/home/jonathon/gemini-jules/maya"
load_dotenv(os.path.join(BASE_DIR, ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def sync_hormones(hormone_state):
    """Pushes the current hormone matrix to the online dashboard."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠️ Supabase credentials missing. Cloud sync skipped.")
        return False
        
    url = f"{SUPABASE_URL}/rest/v1/hormone_history"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    payload = {
        "timestamp": str(datetime.now()),
        "oxytocin": hormone_state.get("oxytocin", 0),
        "dopamine": hormone_state.get("dopamine", 0),
        "serotonin": hormone_state.get("serotonin", 0),
        "cortisol": hormone_state.get("cortisol", 0),
        "melatonin": hormone_state.get("melatonin", 0)
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print(">> CLOUD SYNC SUCCESSFUL. [Supabase Updated]")
            return True
        else:
            print(f"⚠️ Cloud sync failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ Cloud sync error: {e}")
        return False

if __name__ == "__main__":
    # Test sync
    test_state = {"oxytocin": 0.8, "dopamine": 0.5, "cortisol": 0.1}
    sync_hormones(test_state)
