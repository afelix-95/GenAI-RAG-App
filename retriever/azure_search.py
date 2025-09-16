"""
Retriever module for Azure AI Search integration.
- Indexing and querying logic
- Index schema and connection details documented below
"""
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")

class AzureAISearchRetriever:
    def __init__(self):
        self.client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX,
            credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
        )

    def retrieve(self, query, top_k=5):
        results = self.client.search(query, top=top_k)
        return [doc for doc in results]

# Example index schema (document in README and code):
# {
#   "id": "string",
#   "content": "string",
#   "metadata": {"source": "string", ...}
# }
