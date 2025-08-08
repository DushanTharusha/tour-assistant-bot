# backend/rag.py

import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "all-MiniLM-L6-v2"
INDEX_PATH = "backend/data/faiss.index"
CHUNKS_PATH = "backend/data/chunks.json"

class RAGRetriever:
    def __init__(self):
        print("🔌 Loading RAG retriever...")
        self.model = SentenceTransformer(EMBED_MODEL)
        self.index = faiss.read_index(INDEX_PATH)
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
        print(f"✅ Loaded {len(self.chunks)} chunks.")

    def retrieve(self, query, top_k=5):
        query_embedding = self.model.encode([query])[0].astype("float32")
        distances, indices = self.index.search(np.array([query_embedding]), top_k)

        results = []
        for i in indices[0]:
            if i < len(self.chunks):
                results.append(self.chunks[i])
        return results
