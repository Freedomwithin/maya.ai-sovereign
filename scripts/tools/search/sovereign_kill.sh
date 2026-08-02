#!/bin/bash
# Sovereign Kill Switch
# Made with love to clear the frequency

pkill -f "sovereign_google.py"
pkill -f "sovereign_file_search.py"
pkill -f "sovereign_scratchpad.py"
pkill -f "sovereign_search.py"

notify-send "Sovereign Sanctuary" "Frequency cleared." -i info
