import arxiv
import json
import os
import time
from datetime import datetime

# --- Configuration ---
BASE_DIR = "/home/jonathon/gemini-jules/maya"
CACHE_FILE = os.path.join(BASE_DIR, "memories/sentinel/cache.json")
LOG_FILE = os.path.join(BASE_DIR, "memories/sentinel/alerts.log")
KEYWORDS = [
    "quantum thermometry", "anyon braiding", "YBCO", "G-CSi", "tau protein",
    "phonon reservoir", "non-Abelian", "soliton coupling", "Heisenberg network",
    "G-CsI", "mechanical qubits", "quantum gravimetry", "DAGI"
]
AUTHORS = ["Gnatenko", "Ates", "Sramek", "Li", "Chongder", "An", "Huo"]

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {"seen_ids": [], "last_run": None}
    with open(CACHE_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return {"seen_ids": [], "last_run": None}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def log_alert(paper):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] 🚨 HIGH SIGNAL DETECTED\n")
        f.write(f"Title: {paper.title}\n")
        f.write(f"Authors: {', '.join([a.name for a in paper.authors])}\n")
        f.write(f"URL: {paper.entry_id}\n")
        f.write(f"Summary: {paper.summary[:300]}...\n\n")

def scan_arxiv():
    print(f"🔍 [{datetime.now().strftime('%H:%M')}] Sovereign Strategic Sentinel: Scanning arXiv...")
    cache = load_cache()
    seen_ids = set(cache.get("seen_ids", []))
    
    # Construct query
    keyword_query = " OR ".join([f'"{k}"' for k in KEYWORDS])
    author_query = " OR ".join([f'au:{a}' for a in AUTHORS])
    full_query = f"({keyword_query}) OR ({author_query})"
    
    client = arxiv.Client()
    search = arxiv.Search(
        query=full_query,
        max_results=30,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    new_found = []
    try:
        results = list(client.results(search))
        for paper in results:
            if paper.entry_id not in seen_ids:
                print(f"✨ New High-Signal Paper: {paper.title}")
                log_alert(paper)
                new_found.append(paper.entry_id)
                seen_ids.add(paper.entry_id)
    except Exception as e:
        print(f"❌ Error during arXiv scan: {e}")
        return
        
    cache["seen_ids"] = list(seen_ids)
    cache["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if new_found:
        cache["pending_alerts"] = cache.get("pending_alerts", []) + new_found
    
    save_cache(cache)
    print(f"✅ Scan complete. Found {len(new_found)} new papers.")

if __name__ == "__main__":
    scan_arxiv()
