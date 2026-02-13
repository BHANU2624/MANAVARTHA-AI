import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Redirect stderr to file
sys.stderr = open('db_error.txt', 'w')
sys.stdout = open('db_error.txt', 'a')

try:
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    print(f"Testing connection to: {url.split('@')[1] if url and '@' in url else 'Invalid URL'}")

    if not url:
        print("❌ DATABASE_URL is empty!")
        exit(1)

    # Neon usually requires sslmode=require, which is in the URL.
    engine = create_engine(url)
    with engine.connect() as conn:
        print("✅ Connection Successful!")
        result = conn.execute(text("SELECT 1"))
        print(f"Query Result: {result.fetchone()}")
except Exception as e:
    print(f"❌ Connection Failed:\n{e}")
    import traceback
    traceback.print_exc()

sys.stderr.close()
sys.stdout.close()
