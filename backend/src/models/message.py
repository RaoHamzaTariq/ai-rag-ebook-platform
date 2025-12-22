from sqlmodel import SQLModel, Field
from sqlalchemy import Index, JSON, Column
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from pydantic import validator

class Message(SQLModel, table=True):
    __table_args__ = (
        Index('idx_messages_conversation_timestamp', 'conversation_id', 'timestamp'),
        Index('idx_messages_user_id_timestamp', 'user_id', 'timestamp'),
    )

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", nullable=False)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    role: str = Field(nullable=False)  # 'user' or 'assistant'
    content: str = Field(nullable=False)
    sources: Optional[List[Dict[str, Any]]] = Field(default=None, sa_column=Column(JSON))  # For RAG sources
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_type: Optional[str] = Field(default=None)  # For tracking which agent was used

    @validator('role')
    def validate_role(cls, v):
        if v not in ['user', 'assistant']:
            raise ValueError('role must be either "user" or "assistant"')
        return v