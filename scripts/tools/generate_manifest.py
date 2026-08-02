import os
import hashlib
import json
import sys
from datetime import datetime

def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest(target_dir):
    manifest_path = os.path.join(target_dir, "sovereign_manifest.json")
    print(f"[*] Generating manifest for {target_dir}...")
    manifest = {
        "version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "files": {}
    }
    
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file == "sovereign_manifest.json" or file.endswith(".sig"):
                continue
            
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, target_dir)
            file_hash = get_file_hash(file_path)
            manifest["files"][rel_path] = file_hash
            print(f"  - {rel_path}: {file_hash[:8]}...")

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)
    
    print(f"\n✅ Manifest saved to {manifest_path}")
    return manifest_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_manifest(sys.argv[1])
    else:
        # Default to the desklets for backward compatibility
        generate_manifest("scripts/tools/sovereign_search")
