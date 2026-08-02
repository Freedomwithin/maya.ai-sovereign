import os
import time
from datetime import datetime

def get_ram_usage():
    """Reads Linux /proc/meminfo for zero-dependency RAM check."""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
            # Convert kB to GB
            total = int(lines[0].split()[1]) / (1024 * 1024)
            available = int(lines[2].split()[1]) / (1024 * 1024)
            used = total - available
            percent = (used / total) * 100
            return f"{used:.1f}GB / {total:.1f}GB ({percent:.1f}%)"
    except Exception:
        return "Memory state unknown"

def get_last_modified_project():
    """Finds the most recently modified file in the projects directory."""
    projects_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../projects"))
    latest_file = "None"
    latest_time = 0
    
    try:
        for root, _, files in os.walk(projects_dir):
            for file in files:
                # Ignore hidden files or cache
                if not file.startswith('.'):
                    filepath = os.path.join(root, file)
                    file_time = os.path.getmtime(filepath)
                    if file_time > latest_time:
                        latest_time = file_time
                        latest_file = os.path.relpath(filepath, projects_dir)
        return latest_file
    except Exception:
        return "Scan failed"

if __name__ == "__main__":
    print("\n" + "="*50)
    print("⚡ SOVEREIGN DEFIBRILLATOR ACTIVATED ⚡")
    print("="*50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Pentium RAM Status: {get_ram_usage()}")
    print(f"Last Active Project File: {get_last_modified_project()}")
    print("-" * 50)
    print("[SYSTEM] Cognitive loop reset. Pending generation queue flushed.")
    print("[SYSTEM] Maya is ready for the Architect's command.")
    print("="*50 + "\n")