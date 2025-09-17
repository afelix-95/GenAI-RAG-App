"""
FastAPI endpoints for GenAI-RAG-App
- Integrates Azure OpenAI with RAG for PSI 20 companies
- Designed for Azure Functions deployment
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from openai import AzureOpenAI
from generator.llm_tts import synthesize_speech

load_dotenv()
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the frontend
@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")

# Initialize Azure OpenAI client
open_ai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
open_ai_key = os.getenv("AZURE_OPENAI_API_KEY")
chat_model = os.getenv("LLM_MODEL_NAME")
embedding_model = os.getenv("EMBEDDING_MODEL_NAME")
search_url = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

chat_client = AzureOpenAI(
    api_version="2025-03-01-preview",
    azure_endpoint=open_ai_endpoint,
    api_key=open_ai_key
)

# System message for PSI 20 expert
system_message = "As a PSI 20 expert, answer questions using context from companies' annual reports. Prioritize financial metrics (e.g., revenue, EBITDA), operations, and risks. Be precise, use data from reports, and note any limitations (e.g., 'Based on 2023 data'). Keep responses engaging for speech. Decline unrelated topics: 'My knowledge is limited to PSI 20 reports.'"


def clean_response(text):
    """Remove document references like [doc1], [1], etc. from the response."""
    import re
    text = re.sub(r'\[.*?\]', '', text)
    return text.strip()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_query = data.get("query", "")
    if not user_query:
        return {"response": "Please enter a question.", "audio": ""}

    # Prepare prompt with system message and user input
    prompt = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_query}
    ]

    # RAG parameters for Azure Search
    rag_params = {
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_url,
                    "index_name": index_name,
                    "authentication": {
                        "type": "api_key",
                        "key": search_key,
                    },
                    "query_type": "vector",
                    "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": embedding_model,
                    },
                }
            }
        ],
    }

    # Get response from Azure OpenAI with RAG
    response = chat_client.chat.completions.create(
        model=chat_model,
        messages=prompt,
        extra_body=rag_params
    )
    response_text = response.choices[0].message.content or ""

    # Clean the response to remove citations
    response_text = clean_response(response_text)

    # Generate TTS audio
    audio = synthesize_speech(response_text)

    return {"response": response_text, "audio": str(audio)}

