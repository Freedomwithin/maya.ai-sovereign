#!/bin/bash
BASE_DIR="/home/jonathon/gemini-jules/maya"
cd $BASE_DIR
export PYTHONPATH=$PYTHONPATH:$BASE_DIR/scripts/tools/search
export DISPLAY=:0
nohup ./venv/bin/python3 scripts/tools/search/sovereign_file_search.py > /dev/null 2>&1 &
exit 0
