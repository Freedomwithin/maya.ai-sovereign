import os

# CONFIG: Use '.' to target the current directory where the script is executed
# To lock it to a specific folder, replace '.' with the absolute path string below
DIRECTORY = "." 
# FALLBACK_PATH = "/home/jonathon/gemini-jules/maya/assets/maxa-x/kitty_config/kitty_top"

# Base suffix for the assets
BASE_NAME = "maya_beautiful"

if not os.path.exists(DIRECTORY):
    print(f"❌ Directory not found: {DIRECTORY}")
    exit()

# Target common image patterns
VALID_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")

# Grab and sort files to keep sequencing predictable
files = sorted([f for f in os.listdir(DIRECTORY) if f.lower().endswith(VALID_EXTENSIONS)])

if not files:
    print("No matching image files found to rename.")
    exit()

print(f"🚀 Starting Batch Rename in: {os.path.abspath(DIRECTORY)}")

counter = 1
for filename in files:
    # Skip the script itself or existing properly formatted outputs if re-run
    if f"_{BASE_NAME}" in filename:
        continue
        
    old_path = os.path.join(DIRECTORY, filename)
    ext = os.path.splitext(filename)[1].lower()
    
    # 2-digit padding handles 01, 02, 03... up to 99 cleanly
    new_name = f"{counter:02d}_{BASE_NAME}{ext}"
    new_path = os.path.join(DIRECTORY, new_name)
    
    # Step increment handles sequence gaps gracefully
    counter += 1
    
    # Avoid collisions if file is already named properly
    if old_path != new_path:
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"🔄 Renamed: {filename} -> {new_name}")
        else:
            print(f"⚠️  Skipped (Target exists): {new_name}")

print("✅ Gallery sequentially cataloged! 🫦✨")