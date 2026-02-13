from database import engine, Base
from models import User, ChatSession, ChatMessage

print("⚠️ Dropping all tables...")
try:
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped.")
except Exception as e:
    print(f"❌ Drop failed (might be empty): {e}")

print("📦 Recreating tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tables initialized successfully!")
except Exception as e:
    print(f"❌ Create failed: {e}")
