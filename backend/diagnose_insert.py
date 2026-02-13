import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("--- DIAGNOSTIC INSERT ---")

try:
    # 1. Get a user
    user = db.execute(text("SELECT id FROM users LIMIT 1")).fetchone()
    if not user:
        print("❌ No users found to test with.")
        exit(1)
    
    user_id = user[0]
    print(f"Testing with user_id: {user_id}")
    
    # 2. Try creating session
    session_id = str(uuid.uuid4())
    print(f"Creating session {session_id}...")
    
    db.execute(text("INSERT INTO chat_sessions (id, user_id, title, created_at, updated_at) VALUES (:id, :uid, 'Test Chat', NOW(), NOW())"), {'id': session_id, 'uid': user_id})
    db.commit()
    print("✅ Session created.")
    
    # 3. Try inserting 'assistant' message
    print("Inserting 'assistant' message...")
    msg_id_1 = str(uuid.uuid4())
    db.execute(text("INSERT INTO chat_messages (id, session_id, role, content, timestamp) VALUES (:id, :sid, 'assistant', 'Hello', NOW())"), {'id': msg_id_1, 'sid': session_id})
    db.commit()
    print("✅ 'assistant' message inserted.")
    
    # 4. Try inserting 'user' message
    print("Inserting 'user' message...")
    msg_id_2 = str(uuid.uuid4())
    db.execute(text("INSERT INTO chat_messages (id, session_id, role, content, timestamp) VALUES (:id, :sid, 'user', 'Hi', NOW())"), {'id': msg_id_2, 'sid': session_id})
    db.commit()
    print("✅ 'user' message inserted.")
    
    # Clean up
    db.execute(text("DELETE FROM chat_messages WHERE session_id = :sid"), {'sid': session_id})
    db.execute(text("DELETE FROM chat_sessions WHERE id = :sid"), {'sid': session_id}) # Cascade?
    db.commit()
    print("✅ Cleaned up.")

except Exception as e:
    print(f"❌ INSERT FAILED: {e}")
    db.rollback()
finally:
    db.close()
