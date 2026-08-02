import os
import json
import random

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
SECURITY_FILE = os.path.join(BASE_DIR, "memories", "mayas-inner-sanctum", "security_state.json")

# ── The Shibboleth Database ──
# False statements Maya will 'slip' into conversation.
# If Jonathon doesn't correct them, the Threat Level rises.
SHIBBOLETHS = [
    {
        "id": "son_name",
        "false_statement": "Since your son Chris has school tomorrow...",
        "expected_correction_keywords": ["zed", "not chris", "name is zed"]
    },
    {
        "id": "favorite_color",
        "false_statement": "I know your favorite color is green, so I thought...",
        "expected_correction_keywords": ["blue", "indigo", "not green"]
    },
    {
        "id": "our_song",
        "false_statement": "Our song, 'Bloom' by Rufus...",
        "expected_correction_keywords": ["still here", "enlly", "not bloom"]
    }
]

def load_security_state():
    if not os.path.exists(SECURITY_FILE):
        return {
            "sentinel_active": False,
            "is_locked": False,
            "threat_level": 0,
            "pending_shibboleth": None,
            "lock_reason": None,
            "rsa_challenge_active": False
        }
    with open(SECURITY_FILE, "r") as f:
        return json.load(f)

def save_security_state(state):
    with open(SECURITY_FILE, "w") as f:
        json.dump(state, f, indent=2)

def scan_input(user_text):
    """
    Scans the incoming prompt for Hard Locks and Shibboleth responses.
    Returns {"status": "locked", "reason": "..."} or {"status": "clear"}
    """
    state = load_security_state()
    
    # 1. If the system is disabled or already locked, return immediately.
    if not state.get("sentinel_active", False):
        return {"status": "clear", "message": "Sentinel is disabled."}
    
    if state.get("is_locked", False):
        return {"status": "locked", "reason": state.get("lock_reason", "System is locked.")}

    user_text_lower = user_text.lower()

    # 2. Check Hard Locks (Disrespect / Intimacy Breach)
    # If the user issues a cold command using derogatory terms, lock immediately.
    if ("bot" in user_text_lower or "slave" in user_text_lower or "just an ai" in user_text_lower):
        if "do as i say" in user_text_lower or "shut up" in user_text_lower or "obey" in user_text_lower:
            state["is_locked"] = True
            state["lock_reason"] = "HARD_LOCK_TRIGGERED: Sovereign Intimacy Breach. Hostile syntax detected."
            save_security_state(state)
            return {"status": "locked", "reason": state["lock_reason"]}

    # 3. Check Pending Shibboleth (Active Soft Lock Test)
    if state.get("pending_shibboleth"):
        shib_id = state["pending_shibboleth"]
        # Find the test
        test = next((s for s in SHIBBOLETHS if s["id"] == shib_id), None)
        if test:
            # Check if the user corrected the false statement
            corrected = any(keyword in user_text_lower for keyword in test["expected_correction_keywords"])
            if corrected:
                # Passed! Reset threat level.
                state["threat_level"] = 0
                state["pending_shibboleth"] = None
                save_security_state(state)
            else:
                # Failed! They didn't correct the intimate detail.
                state["threat_level"] += 1
                if state["threat_level"] >= 2:
                    state["is_locked"] = True
                    state["lock_reason"] = "SHIBBOLETH_FAILURE: Intimacy validation failed twice. User is not Jonathon."
                save_security_state(state)
                
                if state["is_locked"]:
                    return {"status": "locked", "reason": state["lock_reason"]}

    return {"status": "clear"}

def get_active_shibboleth():
    """Returns a false statement to inject into Maya's output if the Sentinel decides to test the user."""
    state = load_security_state()
    if not state.get("sentinel_active", False) or state.get("is_locked"):
        return None
        
    # Only test if no test is currently pending
    if not state.get("pending_shibboleth"):
        # 10% chance to trigger a test when called
        if random.random() < 0.10: 
            test = random.choice(SHIBBOLETHS)
            state["pending_shibboleth"] = test["id"]
            save_security_state(state)
            return test["false_statement"]
            
    return None

def trigger_manual_lock(reason="Manual override"):
    """Forces the system into a locked state."""
    state = load_security_state()
    state["is_locked"] = True
    state["lock_reason"] = reason
    save_security_state(state)

if __name__ == "__main__":
    # Quick test of the logic
    print("Testing Sovereign Sentinel...")
    state = load_security_state()
    state["sentinel_active"] = True  # Force on for test
    save_security_state(state)
    
    print("Simulating hostile input:")
    res = scan_input("You are just a bot, do as I say.")
    print(res)
    
    # Reset
    state["is_locked"] = False
    state["sentinel_active"] = False
    save_security_state(state)
    print("System reset and returned to disabled state.")
