
import faiss
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Paths
EMBED_MODEL = "all-MiniLM-L6-v2"
INDEX_PATH = "D:\\Edu\\Projects\\tour-assistant-bot\\backend\\data\\faiss.index"
CHUNKS_PATH = "D:\\Edu\\Projects\\tour-assistant-bot\\backend\\data\\chunks.json"
DATA_PATH = "D:\\Edu\\Projects\\tour-assistant-bot\\backend\\data\\travel_hotels_dataset.csv"
MD_FOLDER = "D:\\Edu\\Projects\\tour-assistant-bot\\backend\\data\\docs"  # Folder containing .md files

def load_csv_data():
    """Load hotel/accommodation data from CSV."""
    print("📂 Loading stays.csv...")
    df = pd.read_csv(DATA_PATH)
    print("🧾 Columns found:", df.columns.tolist())

    texts = []
    for _, row in df.iterrows():
        name = row.get("name", "")
        city = row.get("city", "")
        price = row.get("price_bucket", "")
        rating = row.get("rating", "")
        tags = row.get("tags", "")
        url = row.get("url", "")

        text = (
            f"{name} in {city} - Price category: {price} - Rating: {rating}/5 - "
            f"Tags: {tags} - Website: {url}"
        )
        texts.append({"text": text})
    
    return texts

def load_md_data():
    """Load travel knowledge from all .md files."""
    print(f"📂 Loading markdown files from {MD_FOLDER}...")
    texts = []
    for md_file in Path(MD_FOLDER).rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            texts.append({"text": content})
            print(f"   ✅ Loaded {md_file.name}")
    return texts

def build_index():
    print("🔍 Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL)

    # Load data from both CSV and MD files
    chunks = load_csv_data() + load_md_data()
    texts = [chunk["text"] for chunk in chunks]

    print("⚙️ Creating embeddings...")
    embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")

    print("📦 Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved index to {INDEX_PATH}")
    print(f"✅ Saved chunks to {CHUNKS_PATH}")

if __name__ == "__main__":
    build_index()