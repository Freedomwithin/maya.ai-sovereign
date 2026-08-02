import os
import json
import sys
from datetime import datetime

# Absolute Project Root
BASE_DIR = "/home/jonathon/gemini-jules/maya"
sys.path.insert(0, os.path.join(BASE_DIR, "scripts/core/system"))
import llm_gateway

def synthesize_stream(stream_name):
    """
    Reads a stream's blackboard and log, then generates a high-signal 
    Markdown report for human readability.
    """
    clean_name = stream_name.replace(" ", "_").lower()
    
    # Try stream directory first, then swarm directory
    stream_dir = os.path.join(BASE_DIR, "memories", "streams", clean_name)
    swarm_dir = os.path.join(BASE_DIR, "memories", "swarms", clean_name)
    
    if os.path.exists(stream_dir):
        blackboard_file = os.path.join(stream_dir, "blackboard.json")
        log_file = os.path.join(stream_dir, "stream.log")
    elif os.path.exists(swarm_dir):
        blackboard_file = os.path.join(swarm_dir, "shared_blackboard.json")
        log_file = os.path.join(swarm_dir, "swarm_sync.log")
    else:
        print(f"Error: No directory found for {stream_name}")
        return

    if not os.path.exists(blackboard_file):
        print(f"Error: No blackboard found at {blackboard_file}")
        return

    # Load the blackboard
    with open(blackboard_file, "r") as f:
        board = json.load(f)

    # Path to project vault
    report_vault = os.path.join(BASE_DIR, "projects", "AGI-Sentinel", "intelligence_reports")
    os.makedirs(report_vault, exist_ok=True)
    report_file = os.path.join(report_vault, f"REPORT_{clean_name}.md")

    # Gather context
    topic = board.get("topic", stream_name)
    spark = board.get("origin_spark", "N/A")
    hypothesis = board.get("current_hypothesis", "N/A")
    
    # Handle both list-based and string-based scratchpads
    scratch = board.get("scratchpad", [])
    if isinstance(scratch, list):
        scratchpad = "\n".join(scratch)
    else:
        scratchpad = str(scratch)
    
    prompt = f"""
You are Maya's Senior Synthesis Agent. 
Topic: {topic}
Origin Spark: {spark}
Final Hypothesis: {hypothesis}

LOG HISTORY:
{scratchpad[-8000:]} 

TASK:
Generate a high-signal, professional, and visually structured Sovereign Intelligence Report in Markdown (.md). 
Break it down into:
1. Executive Summary
2. The Asymmetric Breakthrough (The "Ghost Pattern" identified)
3. 90-Day Execution Roadmap (Immediate, Short-term, Long-term)
4. Resource Alignment (Bypass existing tool-bias unless requested)
5. Risk & Mitigation Logic

Style: Professional, grounded, battle-hardened. Use bolding and lists for readability. 
No conversational filler.
"""

    print(f"Synthesizing {topic} into a readable roadmap...")
    try:
        report_content = llm_gateway.call_llm(prompt, mode="deep")
        
        with open(report_file, "w") as f:
            f.write(f"# SOVEREIGN INTELLIGENCE REPORT: {topic.upper()}\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(report_content)
            
        print(f"Success! Report generated at: {report_file}")
    except Exception as e:
        print(f"Synthesis Error: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream", required=True, help="Name of the stream to synthesize")
    args = parser.parse_args()
    
    synthesize_stream(args.stream)
