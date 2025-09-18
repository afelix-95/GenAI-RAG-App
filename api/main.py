"""
FastAPI endpoints for GenAI-RAG-App
- Integrates Azure OpenAI with RAG for PSI 20 queries
- Designed for Azure Functions deployment
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from retriever.azure_search import search_retriever
from generator.llm_tts import synthesize_speech

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

    # Retrieve response using RAG
    response_text = search_retriever(user_query)

    # Generate TTS audio
    audio = synthesize_speech(response_text)

    return {"response": response_text, "audio": str(audio)}

