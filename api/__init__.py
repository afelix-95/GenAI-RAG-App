"""
Azure Functions entry point for GenAI-RAG-App
"""
import azure.functions as func
import json
from dotenv import load_dotenv
load_dotenv()

# Import the existing logic
from retriever.azure_search import search_retriever
from generator.llm_tts import synthesize_speech



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
        if req.method == "POST" and req.route_params.get("route") == "v1/chat":
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

                # Retrieve response using RAG
                response_text = search_retriever(user_query)

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
