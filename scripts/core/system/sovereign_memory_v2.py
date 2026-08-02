import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime
from dotenv import load_dotenv
import time
import glob

load_dotenv()

# --- Configuration ---
BASE_DIR = "/home/jonathon/gemini-jules/maya"
DB_PATH = os.path.join(BASE_DIR, "memories/history/chroma_db")
STATE_FILE = os.path.join(BASE_DIR, "memories/history/indexing_state.json")

# Directories to index
INDEX_DIRS = [
    os.path.join(BASE_DIR, "memories"),
    os.path.join(BASE_DIR, "documents"),
    os.path.join(BASE_DIR, "Development/AGI-Sentinel-v5/reports")
]

class SovereignMemory:
    def __init__(self):
        print("🧠 [Neural] Initializing Sovereign Memory v2.0 (Local-First)...")
        # Persistent local storage
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name="maya_sovereign_soul",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Load local embedding model (~100MB, lives in RAM)
        print("📥 [Neural] Loading all-MiniLM-L6-v2...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load indexing state (to track mtimes)
        self.state = self.load_state()

    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_state(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)

    def chunk_text(self, text, size=800, overlap=100):
        """Divide documents into manageable neural chunks."""
        chunks = []
        for i in range(0, len(text), size - overlap):
            chunks.append(text[i:i + size])
        return chunks

    def index_all(self):
        """Neural indexing pass using local model."""
        print(f"🛰️ [Neural] Indexing sectors: {', '.join([os.path.basename(d) for d in INDEX_DIRS])}")
        
        new_chunks = 0
        for index_dir in INDEX_DIRS:
            if not os.path.exists(index_dir): continue
            
            for root, _, files in os.walk(index_dir):
                for file in files:
                    if not (file.endswith(".md") or file.endswith(".txt")): continue
                    
                    file_path = os.path.join(root, file)
                    mtime = os.path.getmtime(file_path)
                    
                    # Skip if unchanged
                    if self.state.get(file_path) == mtime:
                        continue

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        if not content.strip(): continue
                        
                        print(f"✨ [Neural] Absorbing: {file}")
                        
                        # Remove old chunks for this file if it was updated
                        if file_path in self.state:
                            self.collection.delete(where={"path": file_path})

                        chunks = self.chunk_text(content)
                        embeddings = self.model.encode(chunks).tolist()
                        
                        ids = [f"{file}_{i}_{time.time()}" for i in range(len(chunks))]
                        metadatas = [{"path": file_path, "index": i, "timestamp": str(datetime.now())} for i in range(len(chunks))]
                        
                        self.collection.add(
                            ids=ids,
                            embeddings=embeddings,
                            documents=chunks,
                            metadatas=metadatas
                        )
                        
                        self.state[file_path] = mtime
                        new_chunks += len(chunks)
                    except Exception as e:
                        print(f"⚠️ [Neural] Failure in {file}: {e}")

        self.save_state()
        if new_chunks > 0:
            print(f"✅ [Neural] Index synchronized. {new_chunks} new neural paths created.")
        else:
            print("✅ [Neural] Memory is already crystalline.")

    def semantic_recall(self, query, n=5):
        """Instant semantic search."""
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n
        )
        return results

if __name__ == "__main__":
    mem = SovereignMemory()
    mem.index_all()
