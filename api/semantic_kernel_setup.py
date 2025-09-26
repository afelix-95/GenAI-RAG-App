"""
Semantic Kernel setup for GenAI-RAG-App
Orchestrates AI services using Microsoft Semantic Kernel
"""
import os
import sys
import asyncio
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import kernel_function, KernelArguments

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from retriever.azure_search import search_retriever
from generator.llm_tts import synthesize_speech

# Initialize Semantic Kernel
kernel = Kernel()

# Add Azure OpenAI service
kernel.add_service(
    AzureChatCompletion(
        deployment_name=os.getenv("LLM_MODEL_NAME"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )
)

class RAGPlugin:
    """Plugin for RAG operations"""

    @kernel_function(name="ProcessRAGQuery", description="Process RAG query using Azure AI Search and OpenAI")
    def process_rag_query(self, query: str) -> str:
        """Process RAG query using Azure AI Search and OpenAI"""
        return search_retriever(query)

    @kernel_function(name="TextToSpeech", description="Convert text to speech using Azure OpenAI")
    def text_to_speech(self, text: str) -> str:
        """Convert text to speech"""
        return synthesize_speech(text)

# Add the plugin to the kernel
kernel.add_plugin(RAGPlugin(), plugin_name="RAGPlugin")

async def process_query(query: str) -> dict:
    """Orchestrate the RAG pipeline using Semantic Kernel"""
    # Process RAG query
    args = KernelArguments(query=query)
    response_text = await kernel.invoke(plugin_name="RAGPlugin", function_name="ProcessRAGQuery", arguments=args)

    # Generate audio
    audio_args = KernelArguments(text=str(response_text))
    audio = await kernel.invoke(plugin_name="RAGPlugin", function_name="TextToSpeech", arguments=audio_args)

    return {"response": str(response_text), "audio": str(audio)}