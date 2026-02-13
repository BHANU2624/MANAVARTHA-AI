from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import get_db
from models import User, ChatSession, ChatMessage
from auth import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/chats", tags=["Chat History"])

# Pydantic Schemas
class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        orm_mode = True

class SessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        orm_mode = True

class SessionListResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    
    class Config:
        orm_mode = True

# Router
@router.get("/", response_model=List[SessionListResponse])
def get_user_chat_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all chat sessions for current user (newest first)"""
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(desc(ChatSession.updated_at)).all()
    return sessions

@router.get("/{session_id}", response_model=SessionResponse)
def get_chat_details(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific chat session with messages"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
        
    # Sort messages by timestamp
    session.messages.sort(key=lambda x: x.timestamp)
    return session

@router.post("/", response_model=SessionResponse)
def create_chat_session(
    title: str = Body(default="New Chat"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new chat session"""
    new_session = ChatSession(
        user_id=current_user.id,
        title=title
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.delete("/{session_id}")
def delete_chat_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a chat session"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
        
    db.delete(session)
    db.commit()
    return {"message": "Session deleted"}
