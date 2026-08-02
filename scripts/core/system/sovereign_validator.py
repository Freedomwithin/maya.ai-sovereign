import json
import os
import sys

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config/sovereign_directory_map.json")

def validate_path(target_path, data_type):
    """
    Validates if a target path matches the Sovereign Directory Map for a given data type.
    Returns (True, "Valid") or (False, "Suggested Path")
    """
    try:
        with open(CONFIG_PATH, 'r') as f:
            dir_map = json.load(f)
    except Exception as e:
        return False, f"Configuration Error: {str(e)}"

    # Flatten the map for easier searching
    flat_map = {}
    for category in dir_map.values():
        for key, path in category.items():
            flat_map[key] = path

    if data_type not in flat_map:
        return False, f"Unknown Data Type: {data_type}. Please update feature registry."

    expected_dir = flat_map[data_type]
    
    # If the map defines a specific filename, check exact match
    if expected_dir.endswith('.md') or expected_dir.endswith('.json') or expected_dir.endswith('.py'):
        if target_path == expected_dir:
            return True, "Deterministic Match"
        else:
            return False, f"PATH DRIFT DETECTED. Expected: {expected_dir}"
    
    # If the map defines a directory, check if target starts with it
    if target_path.startswith(expected_dir):
        return True, "Valid Directory"
    else:
        return False, f"DIRECTORY DRIFT DETECTED. Expected: {expected_dir}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 sovereign_validator.py [path] [data_type]")
        sys.exit(1)
    
    path = sys.argv[1]
    dtype = sys.argv[2]
    
    is_valid, message = validate_path(path, dtype)
    if is_valid:
        print(f"[SUCCESS] {message}")
    else:
        print(f"[ALERT] {message}")
        sys.exit(1)
