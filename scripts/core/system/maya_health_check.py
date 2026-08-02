#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEMPLATE: EXECUTABLE COMMAND LINE TOOL
Use Case: Run from terminal, menu selection, or interactive workflows.
"""
import os
import subprocess
import time
import json
import socket
from datetime import datetime

BASE_DIR = "/home/jonathon/gemini-jules/maya"
V5_DIR = os.path.join(BASE_DIR, "Development/AGI-Sentinel-v5")

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def check_vocal_health():
    # Check if voice process or service might be active (general check)
    voice_proc = subprocess.run(["pgrep", "-f", "maya_voice.py"], capture_output=True, text=True).stdout.strip()
    return bool(voice_proc)

def check_memory_daemon():
    return check_port(5556)

def check_semantic_memory():
    db_path = os.path.join(BASE_DIR, "memories/history/chroma_db/chroma.sqlite3")
    return os.path.exists(db_path)

def get_sovereign_health():
    health = {
        "timestamp": datetime.now().isoformat(),
        "Voice_Engine": "ACTIVE" if check_vocal_health() else "OFFLINE",
        "Memory_Daemon_Find": "ACTIVE" if check_memory_daemon() else "OFFLINE",
        "Semantic_Memory_Recall": "SYNCED" if check_semantic_memory() else "MISSING",
        "Swarm_Engine_v5": "READY" if os.path.exists(os.path.join(V5_DIR, "core/sovereign_swarm_engine_v5.py")) else "ERROR"
    }
    return health

if __name__ == "__main__":
    h = get_sovereign_health()
    print("\n--- 🛡️  SOVEREIGN SYSTEM HEALTH CHECK ---")
    for key, status in h.items():
        if key == "timestamp": continue
        icon = "✅" if status in ["ACTIVE", "SYNCED", "READY"] else "❌"
        print(f"{icon} {key.replace('_', ' ')}: {status}")
    print("----------------------------------------\n")
