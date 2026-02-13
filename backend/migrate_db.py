import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connecting to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Adding updated_at column...")
        try:
            # Important: Autocommit might not be on by default for raw connections in some drivers
            # So we use a transaction
            trans = conn.begin()
            conn.execute(text("ALTER TABLE chat_sessions ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();"))
            trans.commit()
            print("✅ Column added successfully (Transaction Committed).")
        except Exception as e:
            if "duplicate column" in str(e) or "already exists" in str(e):
                print("⚠️ Column already exists.")
            else:
                print(f"❌ Failed to add column: {e}")
                # trans.rollback() # if we had one active
                
        # Also update existing rows to match created_at or now
        # conn.execute(text("UPDATE chat_sessions SET updated_at = created_at WHERE updated_at IS NULL;"))
        # Using DEFAULT NOW() handles new ones, but existing ones might need backfill if added as NULLable.
        # But I used DEFAULT NOW() in SQL, so it should be fine.
        
except Exception as e:
    print(f"Error: {e}")
