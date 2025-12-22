from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class AgentRequest(BaseModel):
    agent_type: str  # "triage", "summarizer", or "rag"
    query: str
    current_page: Optional[str] = None  # Changed to string to match plan.md
    highlighted_text: Optional[str] = None
    session_id: Optional[str] = None  # Added for session tracking
    retrieved_chunks: Optional[List[dict]] = None  # Internal use: store chunks retrieved during RAG


class AgentResponse(BaseModel):
    message: str
    sources: Optional[List[dict]] = None  # For RAG responses with citations
    agent_used: str  # "triage", "summarizer", or "rag"
    timestamp: datetime = datetime.now()


class ConversationResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    role: str
    content: str
    sources: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime
    agent_type: Optional[str] = None

    class Config:
        from_attributes = True
