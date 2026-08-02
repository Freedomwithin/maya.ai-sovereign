#!/usr/bin/env python3
"""
Auto Article Summarizer
Grabs the current browser page, sends it to Sublime, runs Maya's paragraph summarizer,
and captures the summary back to clipboard and a file.
"""

import pyautogui
import pyperclip
import subprocess
import time
import os
import sys

def focus_brave():
    """Try to focus the Brave browser window using wmctrl."""
    try:
        result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
        windows = result.stdout.splitlines()
        brave_windows = [w for w in windows if 'brave' in w.lower()]
        if not brave_windows:
            print("Brave window not found. Starting Brave...")
            subprocess.Popen(['brave-browser'])
            time.sleep(2)
            result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
            windows = result.stdout.splitlines()
            brave_windows = [w for w in windows if 'brave' in w.lower()]
            if not brave_windows:
                return False
        win_id = brave_windows[0].split()[0]
        subprocess.run(['wmctrl', '-i', '-a', win_id])
        time.sleep(0.5)
        return True
    except FileNotFoundError:
        print("wmctrl not installed. Please install it: sudo apt install wmctrl")
        return False
    except Exception as e:
        print(f"Error focusing Brave: {e}")
        return False

def main():
    # Focus Brave
    if focus_brave():
        print("✅ Brave window focused.")
    else:
        print("⚠️ Could not auto-focus Brave. You have 5 seconds to click into the browser window.")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

    # 1. Copy entire page (Ctrl+A, Ctrl+C)
    print("📋 Copying entire page from browser...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)

    page_text = pyperclip.paste()
    if not page_text or len(page_text.strip()) < 100:
        print("❌ Error: Clipboard is empty or page too short. Make sure browser is focused and page is loaded.")
        return
    print(f"✅ Copied {len(page_text)} characters.")

    # 2. Open Sublime (new window)
    print("📂 Opening Sublime Text...")
    subprocess.Popen(['subl', '-n'])
    time.sleep(1.5)

    # 3. Paste into Sublime
    print("📝 Pasting into Sublime...")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    # 4. Run Maya paragraph summarizer (Ctrl+Alt+Shift+P)
    print("🤖 Running Maya paragraph summarizer (Ctrl+Alt+Shift+P)...")
    pyautogui.hotkey('ctrl', 'alt', 'shift', 'p')
    print("⏳ Waiting for LLM (10-15 seconds)...")
    time.sleep(12)  # Allow time for the LLM to generate summary

    # 5. Select all and copy the summary
    print("📋 Copying summary from Sublime...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

    summary = pyperclip.paste()
    print("\n" + "="*60)
    print("📄 SUMMARY:")
    print("="*60)
    print(summary)
    print("="*60)

    # Save to file
    save_path = os.path.expanduser("~/maya_summary.txt")
    with open(save_path, "w") as f:
        f.write(summary)
    print(f"💾 Summary saved to {save_path}")

    # Optional: copy summary back to clipboard automatically
    pyperclip.copy(summary)
    print("📋 Summary also copied to clipboard (you can paste anywhere).")

    print("\n✅ Done. You can close Sublime now.")

if __name__ == "__main__":
    main()