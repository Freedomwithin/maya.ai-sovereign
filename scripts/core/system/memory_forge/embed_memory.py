import sys
import os
from sovereign_memory_lite import SovereignMemoryLite

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 embed_memory.py <file_path> [category]")
        sys.exit(1)

    file_path = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else "general"
    
    engine = SovereignMemoryLite()
    result = engine.index_file(file_path, category)
    print(f"[MEMORY FORGE] {result}")

if __name__ == "__main__":
    main()
