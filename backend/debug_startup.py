from rag_engine import initialize_rag
import os
import logging

logging.basicConfig(level=logging.INFO)

print("Starting debug...")
csv_path = os.path.join("data", "all_telugu_chunk_embeddings_clean.csv")
print(f"Path: {csv_path}")
print(f"Exists: {os.path.exists(csv_path)}")

try:
    rag = initialize_rag(csv_path)
    print("Init successful!")
    print(f"Chunks: {len(rag.chunks)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
