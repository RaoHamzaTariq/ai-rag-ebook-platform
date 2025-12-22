"""
Simple test script to verify database connection and schema creation
"""
import asyncio
import os
import sys
from sqlmodel import SQLModel, create_engine, Session

# Add the backend/src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.user import User
from models.conversation import Conversation
from models.message import Message

# Use the same database URL as in the config
DATABASE_URL = os.getenv("NEON_DATABASE_URL", "postgresql://localhost:5432/ai_rag_ebook")

async def test_db_connection():
    """Test database connection and schema creation"""
    print("Testing database connection...")

    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        print(f"✓ Engine created with URL: {DATABASE_URL.replace(os.getenv('NEON_DATABASE_URL', ''), '***') if os.getenv('NEON_DATABASE_URL') else DATABASE_URL}")

        # Create all tables
        SQLModel.metadata.create_all(engine)
        print("✓ Tables created successfully")

        # Test creating a session
        with Session(engine) as session:
            print("✓ Database session created successfully")

            # Test that we can query for users (should return empty list)
            users = session.query(User).limit(1).all()
            print(f"✓ Query test successful - found {len(users)} users")

        print("\n✓ Database connection test completed successfully!")
        return True

    except Exception as e:
        print(f"✗ Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_db_connection())