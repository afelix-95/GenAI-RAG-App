import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

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

# Function to clean response text
def clean_response(text):
    """Remove document references like [doc1], [1], etc. from the response."""
    import re
    text = re.sub(r'\[.*?\]', '', text)
    return text.strip()

def search_retriever(user_query):
    """Retrieve relevant documents from Azure Search using vector search and return query response."""
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

    return response_text