import sys
import json
from sovereign_memory_lite import SovereignMemoryLite

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query_soul.py <query_string>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    engine = SovereignMemoryLite()
    results = engine.recall(query)
    
    if not results:
        print("[READER] No matching memories found in the lattice.")
    else:
        print(f"[READER] Found {len(results)} relevant fragments:")
        for res in results:
            print(f"\n--- {res['path']} (Score: {res['score']}) ---")
            print(res['preview'])

if __name__ == "__main__":
    main()
