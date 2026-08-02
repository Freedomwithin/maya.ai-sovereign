#!/usr/bin/env python3
import sys
import os
import re

def sequential_rename(dir_path):
    if not os.path.exists(dir_path):
        print(f"Error: Directory not found: {dir_path}")
        return

    print(f"Processing directory: {dir_path}")

    # Get all files and sort them alphabetically
    try:
        files = sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
    except Exception as e:
        print(f"Error reading directory: {e}")
        return

    counter = 1
    for filename in files:
        # Skip hidden files
        if filename.startswith('.'):
            continue
            
        filepath = os.path.join(dir_path, filename)
        
        # Remove any existing leading numbers and dashes/underscores (e.g., "01_", "02-")
        clean_name = re.sub(r'^\d+[-_]+', '', filename)
        
        # Create the new sequential name
        new_name = f"{counter:02d}-{clean_name}"
        new_filepath = os.path.join(dir_path, new_name)
        
        # Avoid renaming to the exact same name
        if filepath != new_filepath:
            os.rename(filepath, new_filepath)
            print(f"Renamed: {filename} -> {new_name}")
        else:
            print(f"Kept: {filename}")
            
        counter += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sequential_rename.py <directory_path>")
        sys.exit(1)
        
    target_dir = sys.argv[1]
    sequential_rename(target_dir)
