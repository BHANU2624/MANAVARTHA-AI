
import os
import sys
import logging
from dotenv import load_dotenv

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import initialize_rag, get_rag_engine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_retrieval():
    try:
        load_dotenv()
        
        # Path to data
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "all_telugu_chunk_embeddings_clean.csv")
        
        print(f"Loading data from: {csv_path}")
        if not os.path.exists(csv_path):
             print("Error: CSV file not found!")
             return

        # Initialize
        rag = initialize_rag(csv_path)
        
        # Test query
        query = "తెలంగాణ వర్షాలు" # Telangana rains
        print(f"\nScanning for query: {query}")
        
        results = rag._retrieve_chunks(query)
        
        print(f"\nTop {len(results)} Results:")
        for text, score in results:
            print(f"Score: {score:.4f} | Text: {text[:100]}...")
            
        if not results:
            print("\nNO RESULTS FOUND. Checking embedding generation...")
            # Try to embed query manually to see if it works
            try:
                emb = rag.cohere_client.embed(texts=[query], model="embed-multilingual-v3.0", input_type="search_query").embeddings[0]
                print(f"Query embedding generated successfully. Shape: {len(emb)}")
                print(f"First 5 dim: {emb[:5]}")
            except Exception as e:
                print(f"Error generating query embedding: {e}")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_retrieval()
