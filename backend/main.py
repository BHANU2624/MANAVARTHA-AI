"""
MANA VARTHA AI - FastAPI Backend
Multilingual Telugu News RAG Application
"""

import os
import logging
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio

from rag_engine import initialize_rag, get_rag_engine
from database import engine, Base, get_db
from routers import auth, chat
from models import User, ChatSession, ChatMessage
from auth import get_current_user

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MANA VARTHA AI",
    description="Multilingual Telugu News RAG Application",
    version="1.0.0"
)

# Include Routers
app.include_router(auth.router)
app.include_router(chat.router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response model
class SearchResponse(BaseModel):
    query: str
    answer: str
    sources: List[str]
    language: Optional[str] = None
    chunks_retrieved: Optional[int] = None
    new_session_title: Optional[str] = None
    session_id: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str
    chunks_loaded: int

# Startup event - Initialize RAG engine & Database
@app.on_event("startup")
async def startup_event():
    """Initialize RAG engine and Database on startup"""
    try:
        # Create Database Tables
        logger.info("📦 Creating Database Tables if not exist...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database Tables Ready")

        # Path to CSV file
        # Path to CSV file OR Chunks Directory
        base_dir = os.path.dirname(__file__)
        csv_path = os.path.join(base_dir, "data", "all_telugu_chunk_embeddings_clean.csv")
        chunks_dir = os.path.join(base_dir, "data", "chunks")

        if os.path.exists(csv_path):
            logger.info(f"📂 Found single dataset file: {csv_path}")
        elif os.path.exists(chunks_dir) and any(f.endswith('.csv') for f in os.listdir(chunks_dir)):
            logger.info(f"📂 Found dataset chunks in: {chunks_dir}")
            csv_path = chunks_dir
        else:
             # Fallback search
             possible_paths = [
                 os.path.join("data", "all_telugu_chunk_embeddings_clean.csv"),
                 os.path.join("backend", "data", "all_telugu_chunk_embeddings_clean.csv"),
                 "all_telugu_chunk_embeddings_clean.csv",
                 os.path.join("data", "chunks"),
                 os.path.join("backend", "data", "chunks")
             ]
             for p in possible_paths:
                 if os.path.exists(p):
                     csv_path = p
                     break

        logger.info(f"🚀 Starting MANA VARTHA AI backend...")
        logger.info(f"📂 Loading data from: {csv_path}")
        
        async def load_rag_bg():
            logger.info("⏳ Starting background RAG data loading...")
            try:
                # Initialize RAG engine in a thread pool to avoid blocking event loop
                await asyncio.to_thread(initialize_rag, csv_path)
                logger.info("✅ RAG Engine Loaded successfully in background!")
            except Exception as e:
                logger.error(f"❌ Background RAG load failed: {e}")

        # Start RAG loading in background
        asyncio.create_task(load_rag_bg())
        
        logger.info("✅ MANA VARTHA AI backend starting (Auth Ready, RAG Loading)...")

        # Start Daily Update Scheduler
        asyncio.create_task(daily_update_task())
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG engine/DB: {e}")
        raise

async def daily_update_task():
    """Background task to update data daily"""
    while True:
        try:
            logger.info("⏳ Waiting 24 hours for next data update...")
            await asyncio.sleep(86400)
            
            logger.info("🔄 Starting Daily Data Update...")
            
            import subprocess
            try:
                subprocess.run(["python", "generate_data.py"], check=True)
                logger.info("✅ Data generation complete.")
            except Exception as subprocess_error:
                 logger.error(f"⚠️ Data generation script failed: {subprocess_error}")
            
            engine = get_rag_engine()
            if engine.reload_data():
                 logger.info("✅ Daily Update Successful: Index Reloaded")
            else:
                 logger.error("❌ Daily Update Failed: Could not reload index")
                 
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"❌ Error in daily update task: {e}")
            await asyncio.sleep(60)

@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "MANA VARTHA AI - Telugu News RAG API",
        "version": "1.0.0",
        "auth_enabled": True
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        engine_rag = get_rag_engine()
        return HealthResponse(
            status="healthy",
            message="RAG engine is operational",
            chunks_loaded=len(engine_rag.chunks)
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/daily-brief")
async def daily_brief(current_user: Optional[User] = Depends(get_current_user)):
    """Generate a daily editorial brief."""
    # Allow even guests? Sure, it's generic content.
    try:
        engine_rag = get_rag_engine()
        result = engine_rag.generate_daily_brief()
        return result
    except Exception as e:
        logger.error(f"Failed to generate brief: {e}")
        raise HTTPException(status_code=500, detail="Could not generate brief")

@app.get("/search", response_model=SearchResponse)
async def search(
    query: str = Query(..., description="User question"),
    session_id: Optional[str] = Query(None, description="Optional Chat Session ID to save history"),
    mode: str = Query("standard", description="Response mode: standard, quick, deep"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user) # Made optional for backward compatibility
):
    """
    Search endpoint - Main RAG query interface
    """
    try:
        if not query or len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        logger.info(f"📥 Received query: {query}")
        
        # Get RAG engine
        engine_rag = get_rag_engine()
        
        # 0. Fetch History if session_id exists
        history_list = []
        if session_id and current_user:
            # We need to fetch messages BEFORE generating the answer
            try:
                # Basic check for ownership/existence
                session = db.query(ChatSession).filter(
                    ChatSession.id == session_id,
                    ChatSession.user_id == current_user.id
                ).first()
                
                if session:
                    # Fetch last 6 messages
                    recent_msgs = db.query(ChatMessage)\
                        .filter(ChatMessage.session_id == session_id)\
                        .order_by(ChatMessage.timestamp.desc())\
                        .limit(6)\
                        .all()
                    
                    # Reverse to chronological order (Oldest -> Newest)
                    for msg in reversed(recent_msgs):
                        history_list.append({
                            "role": msg.role,
                            "content": msg.content
                        })
                else:
                    # Session not found or other issues, just ignore
                    pass
            except Exception as e:
                logger.warning(f"Failed to fetch history: {e}")

        # Generate answer with history
        result = engine_rag.generate_answer(query, mode=mode, history=history_list)
        
        logger.info(f"📤 Returning answer (language: {result['language']})")
        
        # Persistence Logic
        final_session_id = session_id
        
        # Only proceed if we have a user (even if session_id is missing, we can create one)
        if current_user:
            try:
                chat_session = None
                
                # 1. Try to find existing session if an ID was provided
                if session_id:
                    chat_session = db.query(ChatSession).filter(
                        ChatSession.id == session_id,
                        ChatSession.user_id == current_user.id
                    ).first()
                
                # 2. If not found (or no ID), create NEW session
                if not chat_session:
                    logger.info(f"ℹ️ Creating new session for user {current_user.id} (Proposed ID: {session_id} not found/valid)")
                    chat_session = ChatSession(
                        user_id=current_user.id,
                        title="New Chat",
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(chat_session)
                    db.commit()
                    db.refresh(chat_session)
                    final_session_id = chat_session.id
                
                # 3. Save User Query
                user_msg = ChatMessage(
                    session_id=final_session_id,
                    role="user",
                    content=query,
                    timestamp=datetime.utcnow()
                )
                db.add(user_msg)
                
                # 4. Save Assistant Answer
                bot_msg = ChatMessage(
                    session_id=final_session_id,
                    role="assistant",
                    content=result['answer'],
                    timestamp=datetime.utcnow()
                )
                db.add(bot_msg)
                
                # 5. Auto-Title Logic
                # If title is New Chat/empty, generate one
                if chat_session.title in ["New Chat", None, ""]:
                    words = query.split()
                    selected_words = words[:6] # Max 6 words
                    new_title = " ".join(selected_words).title()
                    # Clean up basic punctuation if needed
                    new_title = new_title.strip(".,!?")
                    
                    chat_session.title = new_title
                    chat_session.updated_at = datetime.utcnow()
                    db.add(chat_session)
                    result['new_session_title'] = new_title
                else:
                    # Just update timestamp
                    chat_session.updated_at = datetime.utcnow()
                    db.add(chat_session)

                db.commit()
                
                # Add the actual session ID to the response so frontend can sync
                result['session_id'] = final_session_id
                
            except Exception as db_err:
                logger.error(f"⚠️ Failed to save chat history: {db_err}")
                # Don't fail the request
        else:
            logger.warning("⚠️ No current_user, skipping persistence.")
        
        return SearchResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "error": str(exc)
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )