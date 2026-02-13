import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Database URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback for local testing if not present (helpful for debugging, though we want Postgres)
if not SQLALCHEMY_DATABASE_URL:
    # Default to a local SQLite file if no URL provided (Safety Net)
    # But ideally, we want Postgres.
    print("⚠️ DATABASE_URL not found. Using local SQLite fallback for safety.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./mvai_fallback.db"

# Handle Postgres protocol update (FastAPI uses postgresql://, newer libraries prefer postgresql+psycopg2://)
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create Engine
# If using SQLite: connect_args={"check_same_thread": False} is needed
connect_args = {}
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for Request Scope
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
