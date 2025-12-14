"""
Database initialization module for Better Auth integration with Neon PostgreSQL
"""
import asyncio
import logging
from sqlmodel import SQLModel
from .config.database import engine
from .models.user import User
from .models.conversation import Conversation
from .models.message import Message

# Set up logger
logger = logging.getLogger('database')

async def create_tables():
    """Create all database tables based on SQLModel models"""
    logger.info("Creating database tables...")

    # Create all tables
    SQLModel.metadata.create_all(engine)

    logger.info("Database tables created successfully")

async def init_database():
    """Initialize the database with required schema"""
    try:
        await create_tables()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise

if __name__ == "__main__":
    # If run directly, initialize the database
    asyncio.run(init_database())