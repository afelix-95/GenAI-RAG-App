"""
Semantic Kernel setup for GenAI-RAG-App
Orchestrates AI services using Microsoft Semantic Kernel
"""
import os
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelFunctionFromMethod
from retriever.azure_search import search_retriever
from generator.llm_tts import synthesize_speech

# Initialize Semantic Kernel
kernel = Kernel()

# Add Azure OpenAI service
kernel.add_service(
    AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )
)

# Create RAG skill (combines retrieval and generation)
def process_rag_query(query: str) -> str:
    """Process RAG query using Azure AI Search and OpenAI"""
    return search_retriever(query)

# Create TTS skill
def text_to_speech(text: str) -> str:
    """Convert text to speech"""
    return synthesize_speech(text)

# Register skills
kernel.add_function(
    KernelFunctionFromMethod(method=process_rag_query, plugin_name="RAGPlugin", function_name="ProcessQuery")
)
kernel.add_function(
    KernelFunctionFromMethod(method=text_to_speech, plugin_name="RAGPlugin", function_name="TTS")
)

async def process_query(query: str) -> dict:
    """Orchestrate the RAG pipeline using Semantic Kernel"""
    # Process RAG query
    response_text = await kernel.invoke("RAGPlugin", "ProcessQuery", query=query)

    # Generate audio
    audio = await kernel.invoke("RAGPlugin", "TTS", text=response_text)

    return {"response": str(response_text), "audio": str(audio)}