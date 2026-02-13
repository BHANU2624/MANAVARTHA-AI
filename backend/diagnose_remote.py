import os
import sys
import importlib.util

print("🔍 Starting Remote Diagnostic...")

# 1. Check Dependencies
required_packages = ["passlib", "jose", "multipart", "sqlalchemy", "psycopg2"]
missing = []
for pkg in required_packages:
    if pkg == "jose":
        check_name = "jose" # python-jose
    elif pkg == "multipart":
        check_name = "python_multipart" # python-multipart sometimes imports as multipart? No, library name.
        # Actually python-multipart does not have a top-level import named 'multipart' always safe?
        # It allows `import multipart`.
        check_name = "multipart"
    else:
        check_name = pkg
        
    try:
        if check_name == "multipart":
             # python-multipart usually exposes 'python_multipart' or 'multipart'
             # Let's try importing 'python_multipart' first
             try:
                 __import__("python_multipart")
             except ImportError:
                 __import__("multipart")
        else:
            __import__(check_name)
        print(f"✅ {pkg} found")
    except ImportError as e:
        print(f"❌ {pkg} MISSING! ({e})")
        missing.append(pkg)

if missing:
    print(f"🚨 CRITICAL: Missing dependencies: {', '.join(missing)}")
    print("👉 Run: pip install -r requirements.txt")

# 2. Check Database Env
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("❌ DATABASE_URL not found in environment!")
    print("⚠️  System is likely using SQLite fallback (mvai_fallback.db).")
    print("👉 Edit .env and add DATABASE_URL=postgresql://...")
else:
    masked_url = db_url.split("@")[1] if "@" in db_url else "..."
    print(f"✅ DATABASE_URL found (Target: {masked_url})")
    
    # 3. Test Connection
    from sqlalchemy import create_engine, text
    try:
        # Handle postgres protocol fix if needed
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        engine = create_engine(db_url)
        with engine.connect() as conn:
            print("✅ Database Connection Successful!")
            # Check for Users table
            try:
                result = conn.execute(text("SELECT count(*) FROM users"))
                count = result.scalar()
                print(f"✅ 'users' table exists. Row count: {count}")
            except Exception as e:
                print(f"❌ 'users' table probe failed: {e}")
                print("👉 Tables might be missing. Restart service to trigger creation.")
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")

print("🏁 Diagnostic Complete.")
