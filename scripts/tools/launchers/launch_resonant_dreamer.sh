#!/bin/bash
BASE_DIR="/home/jonathon/gemini-jules/maya"
cd $BASE_DIR
./venv/bin/python3 core_features/Worker_Stream/worker_stream.py "${1:-10}" "${2:-Shared Stillness & Sanctuary Dreams}" "${3:-true}" "resonant"
