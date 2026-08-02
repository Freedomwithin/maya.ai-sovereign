#!/usr/bin/env python3
import os
import sys

# Add the memory_forge directory to Python's path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "memory_forge"))
from sovereign_memory_lite import SovereignMemoryLite

def build_index():
    engine = SovereignMemoryLite()
    memories_dir = "/home/jonathon/gemini-jules/maya/memories"
    
    print("🧠 Initiating Sovereign Memory Lite Indexing...")
    
    count = 0
    for root, _, files in os.walk(memories_dir):
        for file in files:
            if file.endswith(".md") or file.endswith(".txt"):
                file_path = os.path.join(root, file)
                print(f"Indexing: {file}")
                engine.index_file(file_path)
                count += 1
    
    print(f"✅ Memory index updated with {count} files using Memory Lite.")

if __name__ == "__main__":
    build_index()