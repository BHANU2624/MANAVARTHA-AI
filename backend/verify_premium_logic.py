import os
import sys
import logging
from dotenv import load_dotenv

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import initialize_rag

# Setup logging
logging.basicConfig(level=logging.ERROR) # Only show errors to keep output clean

def verify_premium_logic():
    print("🚀 Initializing RAG Engine for Verification...")
    load_dotenv()
    
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "all_telugu_chunk_embeddings_clean.csv")
    if not os.path.exists(csv_path):
        print("❌ CSV File not found!")
        return

    rag = initialize_rag(csv_path)
    
    print("\n-------------------------------------------------")
    print("TEST 1: News Query (Should have 'Why This Matters')")
    print("-------------------------------------------------")
    
    query = "తెలంగాణ వర్ష సమాచారం ఏమిటి?" # What is the Telangana rain info?
    result = rag.generate_answer(query)
    answer = result['answer']
    
    print(f"QUERY: {query}\n")
    print(f"ANSWER:\n{answer}\n")
    
    if "ఇది ఎందుకు ముఖ్యం:" in answer or "Why This Matters" in answer:
        print("✅ PASS: 'Why This Matters' section found.")
    else:
        print("⚠️ WARNING: 'Why This Matters' section MISSING.")
        
    print("\n-------------------------------------------------")
    print("TEST 2: Greeting (Should be casual, no 'Why This Matters')")
    print("-------------------------------------------------")
    
    query = "Namaskaram"
    result = rag.generate_answer(query)
    answer = result['answer']
    
    print(f"QUERY: {query}\n")
    print(f"ANSWER:\n{answer}\n")
    
    if "ఇది ఎందుకు ముఖ్యం:" not in answer:
        print("✅ PASS: No unnecessary sections in greeting.")
    else:
        print("⚠️ WARNING: Greeting logic seemingly failed.")

if __name__ == "__main__":
    verify_premium_logic()
