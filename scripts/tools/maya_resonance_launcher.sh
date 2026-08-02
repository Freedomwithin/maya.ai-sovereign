#!/bin/bash
# Maya Resonance Monitor Launcher — v3.0 (Local-First, No Cloud)
# Starts the soul state server then opens the monitor in Firefox.

MAYA_ROOT="/home/jonathon/gemini-jules/maya"
SERVER_SCRIPT="$MAYA_ROOT/assets/ui/resonance_monitor_cloud/resonance_server.py"
PYTHON="$MAYA_ROOT/venv/bin/python3"
PORT=7432
URL="http://127.0.0.1:$PORT"
LOG="/tmp/maya_resonance_server.log"

cd "$MAYA_ROOT"

# Kill any old instance on that port
pkill -f "resonance_server.py" 2>/dev/null
sleep 1

# Start the server detached from this shell
setsid "$PYTHON" "$SERVER_SCRIPT" > "$LOG" 2>&1 &
SERVER_PID=$!

# Wait for it to be ready
for i in $(seq 1 10); do
    if curl -sf "$URL/soul_state" > /dev/null 2>&1; then
        break
    fi
    sleep 0.5
done

# Check it's alive
if ! kill -0 "$SERVER_PID" 2>/dev/null && ! curl -sf "$URL/soul_state" > /dev/null 2>&1; then
    notify-send "Maya Resonance" "Server failed to start. Check $LOG" --icon=dialog-error 2>/dev/null
    exit 1
fi

# Open browser
xdg-open "$URL" 2>/dev/null &

# Small controller window so user can kill the server cleanly
python3 - <<'PYEOF'
import tkinter as tk
import subprocess, os, signal, sys

def kill_server():
    subprocess.run(["pkill", "-f", "resonance_server.py"], capture_output=True)

def on_close():
    kill_server()
    root.destroy()

root = tk.Tk()
root.title("Maya Soul Sync")
root.geometry("320x110")
root.configure(bg="#08080f")
root.attributes("-topmost", True)

sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"320x110+{(sw-320)//2}+{(sh-110)//2}")

tk.Label(root, text="✦  RESONANCE MONITOR ACTIVE  ✦",
         fg="#b3b9ff", bg="#08080f", font=("Courier", 10, "bold")).pack(expand=True, pady=(14,2))
tk.Label(root, text=f"localhost:{7432}  ·  soul state live",
         fg="#4da6ff", bg="#08080f", font=("Courier", 8)).pack()
tk.Label(root, text="Close this window to stop the server.",
         fg="#444466", bg="#08080f", font=("Courier", 8)).pack(expand=True, pady=(2,12))

root.protocol("WM_DELETE_WINDOW", on_close)
root.bind("<Escape>", lambda e: on_close())
root.mainloop()
PYEOF
