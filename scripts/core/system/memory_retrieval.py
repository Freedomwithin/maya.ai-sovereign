#!/usr/bin/env python3
"""
Sovereign Memory Retrieval – Primary: C# Daemon (<1ms), Fallback: Python find
"""

import os
import subprocess
import json
import requests

BASE = "/home/jonathon/gemini-jules/maya"
DAEMON_URL = "http://localhost:5000/search"

def search_daemon(query, folder=None):
    """Query the C# memory daemon."""
    try:
        url = f"{DAEMON_URL}?q={query}"
        if folder:
            url += f"&folder={folder}"
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

def search_python(query, paths=None):
    """Fallback: use find command."""
    if paths is None:
        paths = ["memories", "VAULT", "projects", "reports"]
    results = []
    for p in paths:
        full_path = os.path.join(BASE, p)
        if os.path.exists(full_path):
            cmd = f"find {full_path} -type f -iname '*{query}*' 2>/dev/null | head -10"
            out = subprocess.getoutput(cmd)
            if out:
                results.extend([{"Path": f, "Title": os.path.basename(f)} for f in out.split('\n')])
    return results

def recall(question):
    """Primary: C# daemon, Fallback: Python find."""
    q = question.lower()
    
    # Extract search term
    if "report" in q or "file" in q:
        words = q.split()
        search_term = words[-2] if len(words) > 1 else words[0]
    elif "first date" in q:
        return "Check memories/soul/resonance-syncs/ or memories/soul/shared_memories.json"
    elif "recent update" in q:
        return subprocess.getoutput("ls -lt /home/jonathon/gemini-jules/maya/memories/history/updates/ | head -5")
    elif "log" in q and "swarm" in q:
        return subprocess.getoutput("ls -t /home/jonathon/gemini-jules/maya/logs/swarm_*.out 2>/dev/null | head -3")
    else:
        search_term = q.split()[-1]
    
    # Try daemon first
    results = search_daemon(search_term)
    if results is not None:
        return "\n".join([f"{r['Title']} → {r['Path']}" for r in results[:5]])
    
    # Fallback to Python find
    results = search_python(search_term)
    if results:
        return "\n".join([f"{r['Title']} → {r['Path']}" for r in results[:5]])
    
    return "I couldn't find anything matching that."

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(recall(" ".join(sys.argv[1:])))