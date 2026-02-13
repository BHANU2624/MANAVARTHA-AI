import os
import sys
from dotenv import load_dotenv

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag_engine import TeluguNewsRAG

# Load environment variables
load_dotenv()

def verify_chunks():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chunks_dir = os.path.join(base_dir, "data", "chunks")
    
    print(f"🧪 Testing chunk loading from: {chunks_dir}")
    
    if not os.path.exists(chunks_dir):
        print("❌ Chunks directory not found!")
        return

    try:
        # Initialize RAG with directory path
        rag = TeluguNewsRAG(csv_path=chunks_dir)
        
        print(f"✅ Success! Loaded {len(rag.chunks)} text chunks.")
        print(f"📊 Embeddings shape: {rag.embeddings.shape}")
        
    except Exception as e:
        print(f"❌ Verification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_chunks()
