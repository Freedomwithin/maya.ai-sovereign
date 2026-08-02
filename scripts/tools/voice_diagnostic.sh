#!/bin/bash
# Maya Voice Diagnostic v1.0

LOG_FILE="/home/jonathon/gemini-jules/maya/assets/maya_voice.log"
VOICE_SCRIPT="/home/jonathon/gemini-jules/maya/scripts/core/voice/maya_voice.py"

echo "=== 🎙️ Maya Voice Diagnostic ==="
echo "Time: $(date)"

# 1. Check for Running Processes
voice_procs=$(ps aux | grep "$VOICE_SCRIPT" | grep -v grep | wc -l)
if [ "$voice_procs" -gt 0 ]; then
    echo "✅ Voice process detected ($voice_procs active)."
else
    echo "❌ No active voice process found."
fi

# 2. Check for Recent Errors in Logs
if [ -f "$LOG_FILE" ]; then
    last_error=$(grep -i "error\|failed\|timeout" "$LOG_FILE" | tail -n 1)
    if [ -n "$last_error" ]; then
        echo "⚠️ Recent error found in logs:"
        echo "   $last_error"
    else
        echo "✅ No errors found in the last 24h logs."
    fi
else
    echo "❌ Log file not found at $LOG_FILE"
fi

# 3. Test Network Connection to Edge-TTS
if ping -c 1 google.com > /dev/null 2>&1; then
    echo "✅ Network connection OK."
else
    echo "❌ Network connection FAILED."
fi

# 4. Attempt a Silent Test
echo "Attempting silent test..."
/home/jonathon/gemini-jules/maya/venv/bin/python3 "$VOICE_SCRIPT" "..." "Rosa_Goddess" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Silent test execution OK."
else
    echo "❌ Silent test execution FAILED."
fi

echo "==============================="
