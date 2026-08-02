#!/usr/bin/env python3
import sys
import os
import re

def smart_rename(dir_path):
    if not os.path.exists(dir_path):
        print(f"Error: Directory not found: {dir_path}")
        return

    print(f"🏛️ Maya's Organizer: Processing {os.path.abspath(dir_path)}")

    try:
        # We sort by modification time so your newest shots stay in order
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(dir_path, x)))
    except Exception as e:
        print(f"Error reading directory: {e}")
        return

    counter = 1
    for filename in files:
        if filename.startswith('.') or filename == sys.argv[0]:
            continue

        filepath = os.path.join(dir_path, filename)
        
        # Cleanup: Remove old "XX_" prefix if it exists to prevent 01_01_image.jpg
        clean_name = re.sub(r'^\d{2,3}_', '', filename)
        
        name, ext = os.path.splitext(clean_name)
        new_name = f"{counter:02d}_{name}{ext}"
        new_filepath = os.path.join(dir_path, new_name)

        if filepath != new_filepath:
            os.rename(filepath, new_filepath)
            print(f"  ✨ {filename} -> {new_name}")
        else:
            print(f"  💎 {filename} (already perfect)")

        counter += 1
    
    print(f"\n[COMPLETE] {counter-1} items woven into order.")

if __name__ == "__main__":
    # If no arg is provided, we default to the current directory ('.')
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    smart_rename(target_dir)
