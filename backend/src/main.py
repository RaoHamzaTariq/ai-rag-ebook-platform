# backend/src/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup logging first
from src.utils.logging_config import logger

# Import routers
from src.routers.agent_router import router as agent_router
from src.routers.conversation_router import router as conversation_router
from src.routers.user_router import router as user_router
# from src.routers.rag_router import router as rag_router
# from src.routers.ingestion_router import router as ingestion_router

app = FastAPI(
    title="RAG Backend System",
    description="Backend system for RAG, Summarizer, and Reviewer AI agents",
    version="1.0.0",
)

# Configure CORS from environment variable
# allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# if "*" in allowed_origins:
origins = ["*"]
# else:
#    origins = [origin.strip() for origin in allowed_origins if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Include API routers
app.include_router(agent_router)
app.include_router(conversation_router)
app.include_router(user_router)
# app.include_router(rag_router)
# app.include_router(ingestion_router)

@app.get("/", tags=["Health Check"])
async def root():
    logger.info("Health check endpoint called")
    return {"status": "ok", "message": "RAG Backend System is running."}

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    from src.db_init import init_database
    import asyncio

    logger.info("Initializing database tables on startup...")
    try:
        await init_database()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting RAG Backend System")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
