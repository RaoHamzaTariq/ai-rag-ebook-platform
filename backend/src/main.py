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

app = FastAPI(
	title="RAG Backend System",
	description="Backend system for RAG, Summarizer, and Reviewer AI agents",
	version="1.0.0",
)

FRONTEND_URL= os.getenv("FRONTEND_URL")
logger.info(FRONTEND_URL)
if not FRONTEND_URL:
    logger.warning("No FRONTEND_URL set. The chatbot will fail at runtime until a key is provided.")


# Configure CORS specifically for your frontend
app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    os.getenv("FRONTEND_URL"),  # https://ai-ebook-platform.vercel.app
    "http://localhost:3000",
    "http://localhost:3001"
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Include API routers
app.include_router(agent_router)
app.include_router(conversation_router)
app.include_router(user_router)

@app.get("/", tags=["Health Check"])
async def root():
    logger.info("Health check endpoint called")
    return {"status": "ok", "message": "RAG Backend System is running."}

@app.on_event("startup")
async def startup_event():
    logger.info("Startup successfully")

if __name__ == "__main__":
    import uvicorn
    import os
    logger.info("Starting RAG Backend System")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)