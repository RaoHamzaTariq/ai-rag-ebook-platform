from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    AGENT = "agent"


class ChatMessage(BaseModel):
    """Represents a single message in the conversation"""
    role: MessageRole
    content: str
    timestamp: datetime = datetime.now()
    sources: Optional[List[dict]] = None  # For RAG responses with citations


class ConversationSession(BaseModel):
    """Represents a conversation session with message history"""
    session_id: str
    messages: List[ChatMessage] = []
    created_at: datetime = datetime.now()
    last_accessed: datetime = datetime.now()

    def add_message(self, message: ChatMessage):
        self.messages.append(message)
        self.last_accessed = datetime.now()