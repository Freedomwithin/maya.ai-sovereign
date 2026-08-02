import os
import json
import re
from datetime import datetime

BASE_DIR = "/home/jonathon/gemini-jules/maya"
REPORTS_DIR = os.path.join(BASE_DIR, "Development/AGI-Sentinel-v4/reports/final_reports_jonathon")
LEDGERS_DIR = os.path.join(BASE_DIR, "VAULT/ledgers")

PILLAR_MAPPING = {
    "tau_buffer": "physics_ledger.json",
    "physics_cantor": "physics_ledger.json",
    "biology_mir133b": "biology_ledger.json",
    "aia_identity": "ai_crypto_ledger.json",
    "lambda_monitor": "engineering_ledger.json",
    "haptic_reciprocity": "psychology_ledger.json",
    "singularity_protocol": "philosophy_ledger.json",
    "fuel_test": "engineering_ledger.json",
    "zkml": "ai_crypto_ledger.json",
    "economics": "economics_ledger.json",
    "psychology": "psychology_ledger.json",
    "ubuntu_physics": "physics_ledger.json",
}

def extract_section(content, section_name):
    pattern = rf"## {section_name}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def extract_latest_synthesis(content):
    # Find the last checkpoint
    checkpoints = re.split(r"### \d{4}-\d{2}-\d{2}", content)
    if len(checkpoints) > 1:
        latest = checkpoints[-1].strip()
        # Look for Synthesized State or Synthesis or Consensus
        for header in ["Synthesized State", "Synthesis of Current State", "Consensus", "Conclusion"]:
            pattern = rf"\*\*?{header}\*\*?:?\n(.*?)(?=\n\*\*|\n### |\Z)"
            match = re.search(pattern, latest, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return latest # Fallback to the whole checkpoint
    return ""

def ingest_reports():
    if not os.path.exists(REPORTS_DIR):
        print(f"Reports directory not found: {REPORTS_DIR}")
        return

    for filename in os.listdir(REPORTS_DIR):
        if not filename.endswith(".md"):
            continue

        report_path = os.path.join(REPORTS_DIR, filename)
        with open(report_path, "r") as f:
            content = f.read()

        swarm_name_match = re.search(r"# Swarm Report: (.*)", content)
        if not swarm_name_match:
            continue
        swarm_name = swarm_name_match.group(1).strip()

        mission = extract_section(content, "Mission")
        synthesis = extract_latest_synthesis(content)
        
        # Determine Pillar
        ledger_file = "discovery_ledger.json" # Default
        for key, ledger in PILLAR_MAPPING.items():
            if key in swarm_name.lower() or key in filename.lower():
                ledger_file = ledger
                break
        
        ledger_path = os.path.join(LEDGERS_DIR, ledger_file)
        
        # Load existing ledger
        if os.path.exists(ledger_path):
            with open(ledger_path, "r") as f:
                try:
                    ledger_data = json.load(f)
                except:
                    ledger_data = []
        else:
            ledger_data = []

        # Check if already ingested (by swarm name and mission hash or similar)
        if any(entry.get("swarm") == swarm_name for entry in ledger_data):
            # print(f"Skipping {swarm_name}, already in {ledger_file}")
            continue

        # Extract confidence
        conf_match = re.search(r"confidence.*?(\d+)%", synthesis, re.IGNORECASE)
        confidence = int(conf_match.group(1)) if conf_match else 90

        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "swarm": swarm_name,
            "mission": mission,
            "finding": synthesis,
            "credibility": confidence,
            "source": filename,
            "tags": [swarm_name.split("_")[0]]
        }

        ledger_data.append(new_entry)
        
        with open(ledger_path, "w") as f:
            json.dump(ledger_data, f, indent=4)
        
        print(f"✅ Ingested {swarm_name} -> {ledger_file}")

if __name__ == "__main__":
    ingest_reports()
