"""
FastAPI endpoints for GenAI-RAG-App
- Integrates Azure OpenAI with RAG for PSI 20 queries using Semantic Kernel
- Designed for Azure Functions deployment
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from semantic_kernel_setup import process_query

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the frontend
@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")

# Serve favicon.ico
@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)  # No Content - prevents repeated requests

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_query = data.get("query", "")
    if not user_query:
        return {"response": "Please enter a question.", "audio": ""}

    # Process query using Semantic Kernel orchestration
    result = await process_query(user_query)

    return result

