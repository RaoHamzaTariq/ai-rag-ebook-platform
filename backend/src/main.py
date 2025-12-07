# src/main.py
from fastapi import FastAPI

app = FastAPI(title="RAG Backend System")

@app.get("/")
async def root():
    return {"status": "RAG Backend System is running"}

