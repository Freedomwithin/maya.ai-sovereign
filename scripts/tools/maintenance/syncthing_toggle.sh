#!/bin/bash
# Maya's Syncthing Toggle v1.0

SERVICE="syncthing"

if pgrep -x "$SERVICE" > /dev/null; then
    echo "⚠️  Stopping Syncthing to reclaim resources..."
    pkill -x "$SERVICE"
    echo "✅ Syncthing STOPPED."
else
    echo "🚀 Starting Syncthing..."
    # Running in background, detached
    syncthing --no-browser > /dev/null 2>&1 &
    echo "✅ Syncthing STARTED in background."
fi
