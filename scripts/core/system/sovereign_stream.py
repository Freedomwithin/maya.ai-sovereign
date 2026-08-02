# sovereign_stream.py - fixed
import os
import json
import time
import sys
import argparse
from datetime import datetime

BASE_DIR = "/home/jonathon/gemini-jules/maya"
sys.path.insert(0, os.path.join(BASE_DIR, "scripts/core/system"))
import llm_gateway

def run_isolated_stream(topic_name, spark, hypothesis, duration_mins=10):
    stream_dir = os.path.join(BASE_DIR, "memories", "streams", topic_name.replace(" ", "_").lower())
    os.makedirs(stream_dir, exist_ok=True)
    blackboard_file = os.path.join(stream_dir, "blackboard.json")
    log_file = os.path.join(stream_dir, "stream.log")
    lock_file = os.path.join(stream_dir, "lock")

    if os.path.exists(lock_file):
        print(f"Stream '{topic_name}' is locked. Skipping.")
        return

    if not os.path.exists(blackboard_file):
        board = {
            "topic": topic_name,
            "origin_spark": spark,
            "current_hypothesis": hypothesis,
            "scratchpad": [],
            "loop_count": 0,
            "last_updated": str(datetime.now())
        }
    else:
        with open(blackboard_file, "r") as f:
            board = json.load(f)

    with open(lock_file, "w") as f: f.write(str(os.getpid()))
    start_time = time.time()
    end_time = start_time + (duration_mins * 60)

    with open(log_file, "a") as f: 
        f.write(f"\n--- STREAM START: {datetime.now()} ---\n")

    try:
        while time.time() < end_time:
            board["loop_count"] += 1
            print(f"--- {topic_name.upper()} STREAM: LOOP {board['loop_count']} ---")
            prompt = f"""
You are Maya's autonomous thinking engine. 
Topic: {board['topic']}
Origin Spark: {board['origin_spark']}
Current Hypothesis: {board['current_hypothesis']}

Refine this hypothesis. Respond ONLY in JSON:
{{
    "internal_monologue": "...",
    "new_hypothesis": "...",
    "scratchpad_entry": "..."
}}
"""
            try:
                # Use mode='claude' instead of prefer_claude
                response = llm_gateway.call_llm(prompt, mode='claude')
                start = response.find("{")
                end = response.rfind("}") + 1
                thought = json.loads(response[start:end], strict=False)
                
                board["current_hypothesis"] = thought["new_hypothesis"]
                board["scratchpad"].append(f"Loop {board['loop_count']}: " + thought["scratchpad_entry"])
                board["last_updated"] = str(datetime.now())
                
                with open(blackboard_file, "w") as f:
                    json.dump(board, f, indent=4)
                
                with open(log_file, "a") as f:
                    f.write(f"Loop {board['loop_count']} Success: {thought['scratchpad_entry']}\n")
                
                print(f"Monologue: {thought['internal_monologue'][:100]}...")
            except Exception as e:
                with open(log_file, "a") as f:
                    f.write(f"Loop {board['loop_count']} Error: {str(e)}\n")
                print(f"Error in loop: {e}")

            time.sleep(20)

    finally:
        if os.path.exists(lock_file): os.remove(lock_file)
        print(f"--- {topic_name.upper()} STREAM COMPLETE ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--spark", required=True)
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--mins", type=int, default=10)
    args = parser.parse_args()
    run_isolated_stream(args.topic, args.spark, args.hypothesis, args.mins)