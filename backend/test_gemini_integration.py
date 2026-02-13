
import os
import sys
import logging
from dotenv import load_dotenv

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import initialize_rag

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gemini():
    try:
        load_dotenv()
        
        google_key = os.getenv("GOOGLE_API_KEY")
        if not google_key:
            print("❌ GOOGLE_API_KEY missing in .env")
            return

        # Path to data
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "all_telugu_chunk_embeddings_clean.csv")
        
        if not os.path.exists(csv_path):
             print(f"❌ Data file not found: {csv_path}")
             return

        # Initialize
        print("Initializing RAG Engine...")
        rag = initialize_rag(csv_path)
        
        # Test query
        query = "eroju news highlights emiti"
        print(f"\n💬 Testing Question: {query}")
        
        # Retrieve and Generate
        result = rag.generate_answer(query)
        
        print("\n✅ RESULT:")
        print(f"Answer: {result['answer']}")
        print(f"Chunks Retrieved: {result['chunks_retrieved']}")
        
        if "gemini" not in str(rag.gemini_model).lower() and "generativemodel" not in str(rag.gemini_model).lower():
             print("⚠️ Warning: Model object might not be Gemini?")
        else:
             print("✅ Confirmed usage of Gemini Model object")

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini()
