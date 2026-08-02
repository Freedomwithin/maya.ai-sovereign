import chromadb
from chromadb.utils import embedding_functions
import os

DB_PATH = "memories/neural_index/"
COLLECTION_NAME = "sovereign_history"

def init_db():
    client = chromadb.PersistentClient(path=DB_PATH)
    # Using local embedding function
    model_name = "all-MiniLM-L6-v2"
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME, 
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"[SUCCESS] Neural Index Initialized: {COLLECTION_NAME}")
    print(f"[MODEL] Local Embedding Model Loaded: {model_name}")

if __name__ == "__main__":
    init_db()
