import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connecting to DB...")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("\n--- TABLE READINESS CHECK ---")
        
        # Check Tables
        tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall()
        print(f"Tables found: {[t[0] for t in tables]}")
        
        # Check counts
        if 'chat_sessions' in [t[0] for t in tables]:
            c_count = conn.execute(text("SELECT COUNT(*) FROM chat_sessions")).scalar()
            print(f"✅ chat_sessions count: {c_count}")
        else:
            print("❌ chat_sessions table MISSING")
            
        if 'chat_messages' in [t[0] for t in tables]:
            m_count = conn.execute(text("SELECT COUNT(*) FROM chat_messages")).scalar()
            print(f"✅ chat_messages count: {m_count}")
        else:
             print("❌ chat_messages table MISSING")

except Exception as e:
    print(f"❌ Connection Failed: {e}")
