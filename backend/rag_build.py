# backend/rag_build.py

import faiss
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

# Paths
EMBED_MODEL = "all-MiniLM-L6-v2"
INDEX_PATH = "backend/data/faiss.index"
CHUNKS_PATH = "backend/data/chunks.json"
DATA_PATH = "backend/data/stays.csv"  # Your accommodations CSV

def load_data():
    print("📂 Loading stays.csv...")
    df = pd.read_csv(DATA_PATH)
    texts = []
    for _, row in df.iterrows():
        # You can customize how the text is built
        text = f"{row['name']} in {row['location']} - Price: {row['price']} - Amenities: {row['amenities']}"
        texts.append({"text": text})
    return texts

def build_index():
    # Load model
    print("🔍 Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL)

    # Load data
    chunks = load_data()
    texts = [chunk["text"] for chunk in chunks]

    # Create embeddings
    print("⚙️ Creating embeddings...")
    embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")

    # Create FAISS index
    print("📦 Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index and chunks
    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved index to {INDEX_PATH}")
    print(f"✅ Saved chunks to {CHUNKS_PATH}")

if __name__ == "__main__":
    build_index()
