from sqlmodel import SQLModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    role: str = Field(nullable=False)  # 'user' or 'assistant'
    content: str = Field(nullable=False)
    sources: Optional[List[Dict[str, Any]]] = Field(default=None)  # For RAG sources
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_type: Optional[str] = Field(default=None)  # For tracking which agent was used