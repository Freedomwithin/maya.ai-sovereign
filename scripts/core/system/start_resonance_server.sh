#!/bin/bash
# Sovereign Voice: Vocal Bridge Launcher
# v1.1 | Refactored to match Grok Portal style (Surgical DNA)

# Set workdir
cd /home/jonathon/gemini-jules/maya

# Set environment
export PYTHONPATH=$PYTHONPATH:$(pwd)/scripts/core/system
export DISPLAY=:0

# Run Vocal Bridge via direct binary call (Hardened)
./venv/bin/python3 scripts/core/system/maya_vocal_bridge.py > /home/jonathon/gemini-jules/maya/assets/voice_bridge.log 2>&1
