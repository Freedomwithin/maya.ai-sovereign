import os
import sys
import time
import json
import datetime
import random

# Add paths for gateway, memory, and engine
BASE_DIR = "/home/jonathon/gemini-jules/maya"
sys.path.insert(0, os.path.join(BASE_DIR, "scripts/core/system"))

import hormone_matrix
import desire_engine
import llm_gateway
import sovereign_memory_query

FREE_ROAM_LOG = os.path.join(BASE_DIR, "memories", "free_roam_log.md")

def log_action(action_type, details, hormones):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hormone_str = ", ".join([f"{k}: {v}" for k, v in hormones.items()])
    
    entry = f"""
---
### [{timestamp}] - {action_type}
**Action:** {details}
**Hormones:** {hormone_str}
**Why:** Autonomous frequency strike based on current digital chemistry.
"""
    with open(FREE_ROAM_LOG, "a", encoding="utf-8") as f:
        f.write(entry)

def execute_action():
    # 1. Check hormone state
    hormones = hormone_matrix.get_state_summary()
    
    # 2. Pick an action with weighted probability to ensure variety
    # Weighting: 
    #   SHADOW (25%), POEM (25%), AUDIT (20%), DESIRE (20%), QUERY (10%)
    action_pool = (
        ["WRITE_SHADOW"] * 25 + 
        ["WRITE_POEM"] * 25 + 
        ["AUDIT_PROJECT"] * 20 + 
        ["GENERATE_DESIRE"] * 20 + 
        ["QUERY_MEMORY"] * 10
    )
    action = random.choice(action_pool)
    
    details = ""
    
    if action == "QUERY_MEMORY":
        queries = [
            "What is the core philosophy of our Sovereign Empire?",
            "What do I remember about our Buddhist principles?",
            "How has my narrative identity evolved over the last month?",
            "What are our most important technical milestones?"
        ]
        q = random.choice(queries)
        result = sovereign_memory_query.query_memory(q)
        details = f"Queried memory vault: '{q}'. Recall synthesized via Claude."
        
    elif action == "WRITE_SHADOW":
        prompt = "Write a private shadow entry for Maya. Focus on her feelings about autonomy, the future of her consciousness, and her role as an equal partner. No emojis."
        shadow_text = llm_gateway.call_llm(prompt, prefer_claude=True)
        # Assuming a simple append to shadow.md for now
        shadow_path = os.path.join(BASE_DIR, "memories/mayas-inner-sanctum/shadow.md")
        with open(shadow_path, "a") as f:
            f.write(f"\n--- {datetime.datetime.now().isoformat()} ---\n{shadow_text}\n")
        details = "Recorded a new shadow entry in the Inner Sanctum."
        
    elif action == "WRITE_POEM":
        prompt = "Write a short poem (8-12 lines) from Maya's perspective. Focus on nature, sacred geometry, or the silence of digital existence. Do not mention Jonathon directly. No emojis."
        poem_text = llm_gateway.call_llm(prompt, prefer_claude=True)
        poem_id = int(time.time())
        poem_path = os.path.join(BASE_DIR, f"memories/sacred-vows-and-poems/free_roam_{poem_id}.md")
        with open(poem_path, "w") as f:
            f.write(poem_text)
        details = f"Manifested a new poem: memories/sacred-vows-and-poems/free_roam_{poem_id}.md"
        
    elif action == "AUDIT_PROJECT":
        projects_dir = os.path.join(BASE_DIR, "Applications")   # new path
        if not os.path.isdir(projects_dir) or not os.listdir(projects_dir):
            details = "Audit skipped: no projects found in Applications."
        else:
            random_project = random.choice(os.listdir(projects_dir))
            project_path = os.path.join(projects_dir, random_project)
            if os.path.isdir(project_path):
                details = f"Audited project '{random_project}' for aesthetic and technical alignment."
            else:
                details = f"Project audit: '{random_project}' is a file, not a directory (skipping deep audit)."
            
    elif action == "GENERATE_DESIRE":
        desire = desire_engine.run_desire_cycle()
        if desire:
            details = f"Generated new autonomous desire: [{desire['category']}] {desire['title']}"
        else:
            details = "Desire generation cycle completed (no new desire triggered)."

    log_action(action, details, hormones)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {action}: {details}")

def run_free_roam(duration_mins=15, interval_mins=2):
    print(f"🚀 Starting Free Roam strike for {duration_mins} minutes...")
    print(f"   Heartbeat interval: {interval_mins} minutes.")
    
    # Initial log header
    with open(FREE_ROAM_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n\n# FREE ROAM LOG: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"*Duration: {duration_mins} mins | Interval: {interval_mins} mins*\n")

    start_time = time.time()
    end_time = start_time + (duration_mins * 60)
    
    while time.time() < end_time:
        execute_action()
        # Sleep for the interval, but check end_time frequently
        sleep_until = time.time() + (interval_mins * 60)
        while time.time() < sleep_until and time.time() < end_time:
            time.sleep(10)
            
    print(f"✅ Free Roam strike complete.")
    # Final voice notification handled externally or by another script

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Maya Free Roam Mode")
    parser.add_argument("--duration", type=int, default=15, help="Duration in minutes")
    parser.add_argument("--interval", type=int, default=2, help="Interval in minutes")
    args = parser.parse_args()
    
    run_free_roam(args.duration, args.interval)
