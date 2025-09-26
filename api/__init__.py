"""
API package for GenAI-RAG-App
Contains both FastAPI and Azure Functions implementations
"""
# Only import azure.functions when running in Azure Functions environment
try:
    import azure.functions as func
    import json

    # Import the Semantic Kernel logic
    from .semantic_kernel_setup import process_query

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

                    # Process query using Semantic Kernel orchestration
                    result = await process_query(user_query)

                    return func.HttpResponse(
                        json.dumps(result),
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

except ImportError:
    # azure.functions not available (running locally with FastAPI)
    pass
