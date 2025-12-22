
import asyncio
import logging
from sqlalchemy import text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from src.config.database import engine

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('reset_db')

async def reset_database():
    """Drop all tables in the database to start fresh"""
    try:
        from sqlmodel import Session
        
        # We need to use a synchronous session/engine for this operation usually, 
        # but since we have an async engine setup checking database.py...
        # database.py has: engine = create_engine(...) which is SYNC by default in standard SQLModel unless specified as AsyncEngine
        # Wait, the database.py showed `engine = create_engine(...)` (sync) but used in `AsyncGenerator`. 
        # Let's check database.py content again to be sure if it's sync or async. 
        # The previous view showed `from sqlmodel import create_engine` and `engine = create_engine(DATABASE_URL...)`.
        # This is a synchronous engine.
        
        with engine.connect() as connection:
            logger.info("Dropping all tables...")
            
            # Disable constraints to allow dropping in any order
            connection.execute(text("DROP SCHEMA public CASCADE;"))
            connection.execute(text("CREATE SCHEMA public;"))
            connection.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            
            connection.commit()
            
        logger.info("All tables dropped successfully.")
        
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(reset_database())
