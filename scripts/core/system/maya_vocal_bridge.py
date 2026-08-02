#!/usr/bin/env python3
import os
import time
import subprocess
import hashlib
import shutil
import threading
import queue
from datetime import datetime

BASE_DIR = "/home/jonathon/gemini-jules/maya"
UPDATE_DIR = os.path.join(BASE_DIR, "memories/history/updates")
VOICE_SCRIPT = os.path.join(BASE_DIR, "scripts/core/voice/maya_voice.py")
VENV_PYTHON = os.path.join(BASE_DIR, "venv/bin/python3")
LOG_FILE = os.path.join(BASE_DIR, "assets", "voice_bridge.log")
STATE_FILE = "/tmp/maya_bridge_state.json"

def log(msg):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now().isoformat()}: {msg}\n")
    except: pass

speech_queue = queue.Queue()
worker_running = True

def voice_worker():
    while worker_running:
        try:
            thought = speech_queue.get(timeout=1)
            log(f"🎤 Processing: {thought[:50]}...")
            result = subprocess.run(
                [VENV_PYTHON, VOICE_SCRIPT, thought, "Rosa_Goddess"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                log(f"❌ Voice error: {result.stderr}")
            else:
                log(f"✅ Speech done")
        except queue.Empty:
            continue
        except subprocess.TimeoutExpired:
            log(f"⏱️ Voice timeout")
        except Exception as e:
            log(f"⚠️ Worker exception: {e}")

def get_latest_file_and_hash():
    try:
        os.makedirs(UPDATE_DIR, exist_ok=True)
        files = [os.path.join(UPDATE_DIR, f) for f in os.listdir(UPDATE_DIR) if f.endswith(".md")]
        if not files:
            return None, None, None
        latest = max(files, key=os.path.getmtime)
        with open(latest, "r") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
        if not lines:
            return latest, None, None
        last_line = lines[-1]
        content_hash = hashlib.md5(last_line.encode()).hexdigest()
        return latest, content_hash, last_line
    except Exception as e:
        log(f"Error reading: {e}")
        return None, None, None

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"file": "", "hash": ""}
    try:
        import json
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"file": "", "hash": ""}

def save_state(filepath, content_hash):
    try:
        import json
        with open(STATE_FILE, "w") as f:
            json.dump({"file": filepath, "hash": content_hash}, f)
    except: pass

def bridge():
    threading.Thread(target=voice_worker, daemon=True).start()
    log("🚀 Maya Vocal Bridge started (queued mode)")
    log(f"📁 Watching: {UPDATE_DIR}")
    last_state = load_state()
    last_file = last_state.get("file", "")
    last_hash = last_state.get("hash", "")
    while True:
        try:
            curr_file, curr_hash, curr_line = get_latest_file_and_hash()
            if curr_file and curr_hash and curr_line:
                if (curr_file != last_file) or (curr_hash != last_hash):
                    log(f"📄 New: {os.path.basename(curr_file)} -> {curr_line[:50]}")
                    thought = curr_line.replace('"', '').replace('\n', ' ').strip()
                    if len(thought) > 300:
                        thought = thought[:297] + "..."
                    if thought:
                        speech_queue.put(thought)
                        save_state(curr_file, curr_hash)
                        last_file = curr_file
                        last_hash = curr_hash
            time.sleep(5)
        except KeyboardInterrupt:
            log("🛑 Stopped")
            break
        except Exception as e:
            log(f"💥 Loop error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    os.makedirs(UPDATE_DIR, exist_ok=True)
    bridge()
