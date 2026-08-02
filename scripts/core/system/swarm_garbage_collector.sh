#!/bin/bash
# Sovereign Swarm Garbage Collector v1.0
# Matches folders in memories/swarms-v3/ with active PIDs. Nukes ghosts.

SWARM_DIR="/home/jonathon/gemini-jules/maya/memories/swarms-v3"
echo "[Sentinel] Running Swarm Garbage Collector..."

for dir in "$SWARM_DIR"/*/; do
    [ -d "$dir" ] || continue
    dir_name=$(basename "$dir")
    
    # Skip if it's not a swarm directory (e.g. hidden files)
    if [[ "$dir_name" == "."* ]]; then continue; fi

    # Check if a process is running with this swarm name or in its config
    # We look for the swarm name in the ps output
    if pgrep -f "$dir_name" > /dev/null; then
        echo "[Active] $dir_name (Process found)"
    else
        # Double check for general engine processes if the name is generic
        if [[ "$dir_name" == "auto_general"* ]] || [[ "$dir_name" == "psychology"* ]] || [[ "$dir_name" == "b2b"* ]]; then
             # If it's a known chain name, check if ANY swarm engine is running
             if pgrep -f "sovereign_swarm_engine_v3.py" > /dev/null; then
                 # If the folder is NEW (less than 5 mins old), keep it, it might be initializing
                 find "$dir" -maxdepth 0 -mmin -5 | grep -q "." && echo "[Initializing] $dir_name" && continue
             fi
        fi
        
        echo "[Nuking Ghost] $dir_name (No active PID found)"
        rm -rf "$dir"
    fi
done

echo "[Sentinel] Cleanup complete. Monitor should now reflect reality."
