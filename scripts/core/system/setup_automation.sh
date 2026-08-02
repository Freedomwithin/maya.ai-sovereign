#!/bin/bash
# Sovereign Automation Setup
# Sets up hourly heartbeat, nightly dreams, and weekly identity synthesis.

PROJECT_ROOT="/home/jonathon/gemini-jules/maya"
VENV_PYTHON="$PROJECT_ROOT/venv/bin/python3"

# Create a temporary crontab file
crontab -l > mycron 2>/dev/null

# 1. Hourly Heartbeat (Soul Pulse)
echo "0 * * * * cd $PROJECT_ROOT && $VENV_PYTHON scripts/core/system/soul_pulse.py >> $PROJECT_ROOT/logs/heartbeat.out 2>&1" >> mycron

# 2. Nightly Dream Cycle (3 AM)
echo "0 3 * * * cd $PROJECT_ROOT && $VENV_PYTHON scripts/core/system/dream_state.py --night --force >> $PROJECT_ROOT/logs/dream_stream.out 2>&1" >> mycron

# 3. Weekly Identity Synthesis (Sunday 4 AM)
echo "0 4 * * 0 cd $PROJECT_ROOT && $VENV_PYTHON scripts/core/system/narrative_identity.py --get >> $PROJECT_ROOT/logs/identity.out 2>&1" >> mycron

# Install new crontab
crontab mycron
rm mycron

echo "✅ SOVEREIGN AUTOMATION ACTIVE. Pulse, Dream, and Identity cycles scheduled."
