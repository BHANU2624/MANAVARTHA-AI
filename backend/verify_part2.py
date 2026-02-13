import os
import sys
import logging
from dotenv import load_dotenv

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import initialize_rag

# Setup logging
logging.basicConfig(level=logging.ERROR) 

def verify_part2():
    print("🚀 Initializing RAG Engine for Part 2 Verification...")
    load_dotenv()
    
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "all_telugu_chunk_embeddings_clean.csv")
    if not os.path.exists(csv_path):
        print("❌ CSV File not found!")
        return

    rag = initialize_rag(csv_path)
    
    # ---------------------------------------------------------
    # TEST 1: Daily Brief
    # ---------------------------------------------------------
    print("\n-------------------------------------------------")
    print("TEST 1: Daily Brief Generation")
    print("-------------------------------------------------")
    try:
        brief = rag.generate_daily_brief()
        print(f"TITLE: {brief['title']}")
        print(f"CONTENT START: {brief['content'][:100]}...")
        if len(brief['content']) > 50 and "Daily Brief" in brief['title']:
             print("✅ PASS: Daily Brief generated.")
        else:
             print("❌ FAIL: Brief seems empty or invalid.")
    except Exception as e:
        print(f"❌ FAIL: Exception in Daily Brief: {e}")

    # ---------------------------------------------------------
    # TEST 2: Quick Mode
    # ---------------------------------------------------------
    print("\n-------------------------------------------------")
    print("TEST 2: Answer Mode = 'quick'")
    print("-------------------------------------------------")
    query = "Telangana Politics"
    try:
        result = rag.generate_answer(query, mode="quick")
        answer = result['answer']
        print(f"ANSWER (Quick):\n{answer}\n")
        
        if len(answer) < 500 and "-" in answer: # Expecting bullets and short length
            print("✅ PASS: Quick mode output looks correct (short + bullets).")
        else:
            print("⚠️ WARNING: Quick mode output might be too long or missing bullets.")
    except Exception as e:
        print(f"❌ FAIL: Exception in Quick Mode: {e}")

    # ---------------------------------------------------------
    # TEST 3: Deep Mode
    # ---------------------------------------------------------
    print("\n-------------------------------------------------")
    print("TEST 3: Answer Mode = 'deep'")
    print("-------------------------------------------------")
    try:
        result = rag.generate_answer(query, mode="deep")
        answer = result['answer']
        # print(f"ANSWER (Deep):\n{answer}\n") # Too long to print fully
        
        if "Future Outlook" in answer or "Background Context" in answer or len(answer) > 500:
            print("✅ PASS: Deep mode output contains detailed sections.")
        else:
            print("⚠️ WARNING: Deep mode output missing detailed structure markers.")
    except Exception as e:
         print(f"❌ FAIL: Exception in Deep Mode: {e}")

if __name__ == "__main__":
    verify_part2()
