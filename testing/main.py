import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Configure CORS
origins = [
    "*",  # Allow all origins (for testing). For production, replace "*" with your frontend URL(s)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Can be list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Railway!"}

if __name__ == "__main__":
    # Railway dynamically provides the PORT
    port = int(os.environ.get("PORT", 8000))  # 8000 fallback for local testing
    uvicorn.run(app, host="0.0.0.0", port=port)
