# backend/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from src.routers.agent_router import router as agent_router
# from src.routers.rag_router import router as rag_router
# from src.routers.ingestion_router import router as ingestion_router

app = FastAPI(
    title="RAG Backend System",
    description="Backend system for RAG, Summarizer and Reviewer AI agents",
    version="1.0.0",
)

# Allow CORS (adjust origins as needed)
origins = [
    # "http://localhost",
    # "http://localhost:3000",
    # Add your frontend URL here
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(agent_router)
# app.include_router(rag_router)
# app.include_router(ingestion_router)

@app.get("/", tags=["Health Check"])
async def root():
    return {"status": "ok", "message": "RAG Backend System is running."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
