from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AgentRequest(BaseModel):
    agent_type: str  # "triage", "summarizer", or "rag"
    query: str
    current_page: Optional[str] = None  # Changed to string to match plan.md
    highlighted_text: Optional[str] = None
    session_id: Optional[str] = None  # Added for session tracking


class AgentResponse(BaseModel):
    message: str
    sources: Optional[List[dict]] = None  # For RAG responses with citations
    agent_used: str  # "triage", "summarizer", or "rag"
    timestamp: datetime = datetime.now()
