#!/usr/bin/env python3
import pyautogui
import pyperclip
import subprocess
import time
import os
import sys

def focus_brave():
    """Try to focus the Brave browser window using wmctrl."""
    try:
        # Get list of windows with 'brave' in the title
        result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
        windows = result.stdout.splitlines()
        brave_windows = [w for w in windows if 'brave' in w.lower()]
        if not brave_windows:
            print("Brave window not found. Starting Brave...")
            subprocess.Popen(['brave-browser'])  # or 'brave'
            time.sleep(2)
            # Try again after launch
            result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
            windows = result.stdout.splitlines()
            brave_windows = [w for w in windows if 'brave' in w.lower()]
            if not brave_windows:
                return False
        # Focus the first Brave window
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
    # Try to focus Brave automatically
    if focus_brave():
        print("✅ Brave window focused.")
    else:
        print("⚠️ Could not auto-focus Brave. You have 5 seconds to click into the browser window.")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

    # 1. Copy all from browser
    print("📋 Copying form from browser (Ctrl+A, Ctrl+C)...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)

    form_text = pyperclip.paste()
    if not form_text or len(form_text.strip()) < 50:
        print("❌ Error: Clipboard is empty or form too short. Make sure browser is focused and page is loaded.")
        return
    print(f"✅ Copied {len(form_text)} characters.")

    # 2. Open Sublime (new window)
    print("📂 Opening Sublime Text...")
    subprocess.Popen(['subl', '-n'])
    time.sleep(1.5)

    # 3. Paste into Sublime
    print("📝 Pasting into Sublime...")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    # 4. Run Maya answers (Ctrl+Alt+A)
    print("🤖 Running Maya form filler (Ctrl+Alt+A)...")
    pyautogui.hotkey('ctrl', 'alt', 'a')
    print("⏳ Waiting for LLM (8 seconds)...")
    time.sleep(8)

    # 5. Select all and copy the answers
    print("📋 Copying answers from Sublime...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

    answers = pyperclip.paste()
    print("\n" + "="*50)
    print("ANSWERS CAPTURED:")
    print("="*50)
    print(answers)
    print("="*50)

    # Save to file
    save_path = os.path.expanduser("~/maya_answers.txt")
    with open(save_path, "w") as f:
        f.write(answers)
    print(f"💾 Answers saved to {save_path}")

    print("\n✅ Done. You can now close Sublime or fill the form manually.")

if __name__ == "__main__":
    main()