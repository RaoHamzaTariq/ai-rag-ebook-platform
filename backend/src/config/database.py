from sqlmodel import create_engine
import os
from typing import Optional, AsyncGenerator
from urllib.parse import urlparse
from sqlalchemy.pool import QueuePool
import logging

# Set up logger for database operations
logger = logging.getLogger('database')

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Parse the database URL to extract connection parameters
parsed_url = urlparse(DATABASE_URL)

# Create engine with async support
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("LOG_LEVEL", "INFO").upper() == "DEBUG",  # Set to False in production
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
    pool_timeout=30,     # 30 seconds timeout for getting connection from pool
    pool_reset_on_return='commit',  # Reset connection on return to pool
)

async def get_db() -> AsyncGenerator:
    """Async dependency for FastAPI to get database session"""
    from sqlmodel import Session
    async with Session(engine) as session:
        logger.info("Database session created")
        yield session

def get_sync_db():
    """Sync dependency for FastAPI to get database session"""
    from sqlmodel import Session
    with Session(engine) as session:
        logger.info("Synchronous database session created")
        yield session

async def init_db():
    """Initialize the database and create tables if they don't exist"""
    from sqlmodel import SQLModel
    from .models.user import User
    from .models.conversation import Conversation
    from .models.message import Message

    logger.info("Initializing database...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database initialized successfully")