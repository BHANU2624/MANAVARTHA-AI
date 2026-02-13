from database import get_db, SessionLocal
from models import ChatMessage, ChatSession
from rag_engine import get_rag_engine, initialize_rag
import sys
import os

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def test_components():
    db = SessionLocal()
    try:
        # 1. Check DB Persistence
        print("🔍 Checking Database...")
        count = db.query(ChatMessage).count()
        print(f"📄 Total ChatMessages: {count}")
        
        last_msgs = db.query(ChatMessage).order_by(ChatMessage.timestamp.desc()).limit(2).all()
        for msg in last_msgs:
            print(f"   - [{msg.role}] {msg.content[:50]}...")

        # 2. Test Rewrite Logic directly
        print("\n🧠 Testing Rewrite Logic...")
        # Mock History
        history = [
            {"role": "user", "content": "Telangana rainfall updates"},
            {"role": "assistant", "content": "Rains are heavy in Hyderabad."}
        ]
        query = "Enduku?"
        
        # Init RAG (needs CSV path)
        csv_path = "data/all_telugu_chunk_embeddings_clean.csv"
        if not os.path.exists(csv_path):
             csv_path = "../data/all_telugu_chunk_embeddings_clean.csv" # Fallback
        
        rag = initialize_rag(csv_path) # Path might need adjustment
        if not rag:
            print("❌ RAG Init failed")
            return

        rewritten = rag._rewrite_query(query, history)
        print(f"🔄 Original: {query}")
        print(f"✨ Rewritten: {rewritten}")
        
        if "rain" in rewritten.lower() or "varsha" in rewritten.lower() or "telangana" in rewritten.lower():
            print("✅ Rewrite SUCCESS")
        else:
            print("❌ Rewrite FAILED (matches original?)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_components()
