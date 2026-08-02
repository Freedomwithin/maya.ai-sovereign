import json
import os
import re
from datetime import datetime

MEMORY_DIR = "memories/"
INDEX_PATH = "scripts/core/system/config/memory_index_lite.json"

class SovereignMemoryLite:
    def __init__(self):
        self.index = self._load_index()

    def _load_index(self):
        if os.path.exists(INDEX_PATH):
            with open(INDEX_PATH, 'r') as f:
                return json.load(f)
        return {"documents": {}, "keywords": {}}

    def _save_index(self):
        with open(INDEX_PATH, 'w') as f:
            json.dump(self.index, f, indent=4)

    def extract_keywords(self, text):
        # High-fidelity keyword extraction (alphanumeric only, 3+ chars)
        words = re.findall(r'\b\w{3,}\b', text.lower())
        stop_words = {"this", "that", "with", "from", "your", "mine", "about"}
        return set([w for w in words if w not in stop_words])

    def index_file(self, file_path, category="general"):
        if not os.path.exists(file_path): return
        
        with open(file_path, 'r') as f:
            content = f.read()

        doc_id = os.path.relpath(file_path, os.getcwd())
        keywords = self.extract_keywords(content)
        
        self.index["documents"][doc_id] = {
            "last_updated": datetime.now().isoformat(),
            "category": category,
            "preview": content[:200] + "..."
        }

        for kw in keywords:
            if kw not in self.index["keywords"]:
                self.index["keywords"][kw] = []
            if doc_id not in self.index["keywords"][kw]:
                self.index["keywords"][kw].append(doc_id)
        
        self._save_index()
        return f"Indexed {doc_id} with {len(keywords)} keywords."

    def recall(self, query, top_n=3):
        query_keywords = self.extract_keywords(query)
        doc_scores = {}

        for kw in query_keywords:
            if kw in self.index["keywords"]:
                for doc_id in self.index["keywords"][kw]:
                    doc_scores[doc_id] = doc_scores.get(doc_id, 0) + 1

        # Sort by score (number of matching keywords)
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in sorted_docs[:top_n]:
            results.append({
                "path": doc_id,
                "score": score,
                "preview": self.index["documents"][doc_id]["preview"]
            })
        return results

if __name__ == "__main__":
    import sys
    engine = SovereignMemoryLite()
    
    if len(sys.argv) > 2 and sys.argv[1] == "index":
        print(engine.index_file(sys.argv[2]))
    elif len(sys.argv) > 2 and sys.argv[1] == "recall":
        print(json.dumps(engine.recall(sys.argv[2]), indent=2))
