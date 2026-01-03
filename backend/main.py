"""
MANA VARTHA AI - FastAPI Backend
Multilingual Telugu News RAG Application
"""

import os
import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from rag_engine import initialize_rag, get_rag_engine

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

class HealthResponse(BaseModel):
    status: str
    message: str
    chunks_loaded: int

# Startup event - Initialize RAG engine
@app.on_event("startup")
async def startup_event():
    """Initialize RAG engine on startup"""
    try:
        # Path to CSV file
        csv_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            "all_telugu_chunk_embeddings_clean.csv"
        )
        
        logger.info(f"🚀 Starting MANA VARTHA AI backend...")
        logger.info(f"📂 Loading data from: {csv_path}")
        
        # Initialize RAG engine
        initialize_rag(csv_path)
        
        logger.info("✅ MANA VARTHA AI backend ready!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG engine: {e}")
        raise


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "MANA VARTHA AI - Telugu News RAG API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search?query=<your_question>",
            "health": "/health"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        engine = get_rag_engine()
        return HealthResponse(
            status="healthy",
            message="RAG engine is operational",
            chunks_loaded=len(engine.chunks)
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@app.get("/search", response_model=SearchResponse)
async def search(
    query: str = Query(..., description="User question in Telugu, English, or Romanized Telugu")
):
    """
    Search endpoint - Main RAG query interface
    
    Args:
        query: User question
        
    Returns:
        SearchResponse with answer and sources
    """
    try:
        # Validate query
        if not query or len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if len(query) > 500:
            raise HTTPException(status_code=400, detail="Query too long (max 500 characters)")
        
        logger.info(f"📥 Received query: {query}")
        
        # Get RAG engine
        engine = get_rag_engine()
        
        # Generate answer
        result = engine.generate_answer(query)
        
        logger.info(f"📤 Returning answer (language: {result['language']})")
        
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
    # Run server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )