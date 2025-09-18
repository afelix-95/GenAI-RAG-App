"""
Azure Functions entry point for GenAI-RAG-App
"""
import azure.functions as func
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Import the existing logic
from retriever.azure_search import search_retriever
from generator.llm_tts import synthesize_speech

# Initialize clients (same as main.py)
open_ai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
open_ai_key = os.getenv("AZURE_OPENAI_API_KEY")
chat_model = os.getenv("TTS_MODEL_NAME")
embedding_model = os.getenv("EMBEDDING_MODEL_NAME")
search_url = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

# System message
system_message = "As a PSI 20 expert, answer questions using context from companies' annual reports. Prioritize financial metrics (e.g., revenue, EBITDA), operations, and risks. Be precise, use data from reports, and note any limitations (e.g., 'Based on 2023 data'). Keep responses engaging for speech. Decline unrelated topics: 'My knowledge is limited to PSI 20 reports.'"

def clean_response(text):
    """Remove document references from response."""
    import re
    text = re.sub(r'\[.*?\]', '', text)
    return text.strip()

async def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Functions HTTP trigger"""

    # Handle CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )

    try:
        # Serve frontend for GET requests to root
        if req.method == "GET" and req.route_params.get("route") in [None, ""]:
            try:
                with open("frontend/index.html", "r", encoding="utf-8") as f:
                    html_content = f.read()
                return func.HttpResponse(
                    html_content,
                    status_code=200,
                    headers={
                        "Content-Type": "text/html",
                        "Access-Control-Allow-Origin": "*"
                    }
                )
            except FileNotFoundError:
                return func.HttpResponse("Frontend not found", status_code=404)

        # Handle favicon
        if req.route_params.get("route") == "favicon.ico":
            return func.HttpResponse(status_code=204)

        # Handle chat API
        if req.method == "POST" and req.route_params.get("route") == "chat":
            try:
                req_body = req.get_json()
                user_query = req_body.get("query", "")

                if not user_query:
                    return func.HttpResponse(
                        json.dumps({"response": "Please enter a question.", "audio": ""}),
                        status_code=200,
                        headers={
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*"
                        }
                    )

                # Use Azure OpenAI with RAG (same logic as main.py)
                from openai import AzureOpenAI

                chat_client = AzureOpenAI(
                    api_version="2024-12-01-preview",
                    azure_endpoint=open_ai_endpoint,
                    api_key=open_ai_key
                )

                prompt = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_query}
                ]

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

                response = chat_client.chat.completions.create(
                    model=chat_model,
                    messages=prompt,
                    extra_body=rag_params
                )

                response_text = response.choices[0].message.content or ""
                response_text = clean_response(response_text)

                # Generate TTS
                audio = synthesize_speech(response_text)

                return func.HttpResponse(
                    json.dumps({"response": response_text, "audio": audio}),
                    status_code=200,
                    headers={
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                )

            except Exception as e:
                return func.HttpResponse(
                    json.dumps({"error": str(e)}),
                    status_code=500,
                    headers={
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                )

        return func.HttpResponse("Not found", status_code=404)

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
