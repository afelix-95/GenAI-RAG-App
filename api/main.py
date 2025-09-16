"""
FastAPI endpoints for GenAI-RAG-App
- Integrates retriever and generator modules
- Designed for Azure Functions deployment
"""
from fastapi import FastAPI, Request
from retriever.azure_search import AzureAISearchRetriever
from generator.llm_tts import LLM_TTS_Generator

app = FastAPI()
retriever = AzureAISearchRetriever()
generator = LLM_TTS_Generator()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_query = data.get("query", "")
    docs = retriever.retrieve(user_query)
    context = "\n".join([doc["content"] for doc in docs])
    prompt = f"Context:\n{context}\n\nUser: {user_query}"
    response_text = generator.generate_response(prompt)
    audio = generator.synthesize_speech(response_text)
    return {"response": response_text, "audio": str(audio)}
