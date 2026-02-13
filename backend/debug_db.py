import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connecting to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    
    if "chat_sessions" in inspector.get_table_names():
        print("Table 'chat_sessions' exists.")
        columns = [col['name'] for col in inspector.get_columns("chat_sessions")]
        print(f"Columns: {columns}")
        if "updated_at" in columns:
            print("✅ updated_at column exists.")
        else:
            print("❌ updated_at column MISSING.")
    else:
        print("❌ Table 'chat_sessions' does NOT exist.")

except Exception as e:
    print(f"Error: {e}")
