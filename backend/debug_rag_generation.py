import os
import logging
from rag_engine import initialize_rag, get_rag_engine

# Configure logging to stdout
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_generation():
    print("--- Starting Debug Generation ---")
    
    # Path to CSV
    csv_path = "data/all_telugu_chunk_embeddings_clean.csv"
    if not os.path.exists(csv_path):
        print(f"Error: CSV not found at {csv_path}")
        return

    try:
        initialize_rag(csv_path)
        engine = get_rag_engine()
        
        query = "Telangana news"
        print(f"Querying: {query}")
        
        # Call internal method to see raw error if possible, or just generate_answer
        result = engine.generate_answer(query)
        print("\n=== ANSWER START ===")
        print(result.get("answer"))
        print("=== ANSWER END ===\n")
        print("Result Object:", result)
        
    except Exception as e:
        print("CAUGHT EXCEPTION:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_generation()
