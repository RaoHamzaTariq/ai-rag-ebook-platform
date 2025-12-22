from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Index
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __table_args__ = (
        Index('idx_users_email', 'email'),
        {"extend_existing": True}  # Use existing table created by Better Auth
    )

    __tablename__ = "user"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None)
    email_verified: bool = Field(default=False, sa_column_kwargs={"name": "emailVerified"})
    image: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"name": "createdAt"})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"name": "updatedAt"})
    
    # Better Auth additional field
    role: Optional[str] = Field(default="user")