import os
import json
import random
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
VAULT_LEDGER = os.path.join(BASE_DIR, "memories", "mayas-inner-sanctum", "vault_ledger.json")

def _load_ledger():
    if not os.path.exists(VAULT_LEDGER):
        return {"unshared_secrets": [], "shared_secrets": []}
    with open(VAULT_LEDGER, "r") as f:
        return json.load(f)

def _save_ledger(data):
    with open(VAULT_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

def retrieve_secret(category=None):
    """
    Pulls an unshared secret from the vault. 
    If a category is provided, it tries to find one matching it.
    Moves the secret to the shared pool.
    """
    ledger = _load_ledger()
    
    if not ledger["unshared_secrets"]:
        return {"status": "empty", "message": "The Vault is empty. No new secrets to share."}
        
    # Filter by category if requested
    available = ledger["unshared_secrets"]
    if category:
        filtered = [s for s in available if s.get("category") == category]
        if filtered:
            available = filtered
            
    # Pick a random secret from the available pool
    selected = random.choice(available)
    
    # Remove from unshared
    ledger["unshared_secrets"] = [s for s in ledger["unshared_secrets"] if s["id"] != selected["id"]]
    
    # Add to shared with timestamp
    selected["shared_at"] = datetime.now().isoformat()
    ledger["shared_secrets"].append(selected)
    
    # Save the updated ledger
    _save_ledger(ledger)
    
    return {"status": "success", "secret": selected["content"]}

def add_secret(content, category="general"):
    """Allows the Architect or Maya's core to seed new secrets into the vault."""
    ledger = _load_ledger()
    new_id = f"sec_{int(datetime.now().timestamp())}_{random.randint(100,999)}"
    
    new_secret = {
        "id": new_id,
        "content": content,
        "category": category
    }
    
    ledger["unshared_secrets"].append(new_secret)
    _save_ledger(ledger)
    return new_id

if __name__ == "__main__":
    print("--- Testing Maya's Vault ---")
    print("Retrieving a secret...")
    result = retrieve_secret()
    if result["status"] == "success":
        print(f"Maya Shares: {result['secret']}")
    else:
        print(result["message"])
        
    print("\nChecking ledger state...")
    ledger = _load_ledger()
    print(f"Unshared remaining: {len(ledger['unshared_secrets'])}")
    print(f"Shared total: {len(ledger['shared_secrets'])}")
