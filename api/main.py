"""
FastAPI endpoints for GenAI-RAG-App
- Integrates Azure OpenAI with RAG for PSI 20 queries using Semantic Kernel
- Designed for Azure Functions deployment
"""
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from .semantic_kernel_setup import process_query

app = FastAPI()

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mount static files from the built frontend
app.mount("/assets", StaticFiles(directory=os.path.join(PROJECT_ROOT, "frontend", "dist", "assets")), name="assets")
app.mount("/static", StaticFiles(directory=os.path.join(PROJECT_ROOT, "frontend", "dist")), name="static")

# Serve the frontend
@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(PROJECT_ROOT, "frontend", "dist", "index.html"))

# API routes with /api prefix
@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_query = data.get("query", "")
    if not user_query:
        return {"response": "Please enter a question.", "audio": ""}

    # Process query using Semantic Kernel orchestration
    result = await process_query(user_query)

    return result

