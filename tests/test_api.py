import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Set mock env vars
os.environ["AZURE_OPENAI_ENDPOINT"] = "test_endpoint"
os.environ["AZURE_OPENAI_API_KEY"] = "test_key"
os.environ["TTS_MODEL_NAME"] = "test_model"
os.environ["EMBEDDING_MODEL_NAME"] = "test_embedding"
os.environ["AZURE_SEARCH_ENDPOINT"] = "test_search"
os.environ["AZURE_SEARCH_API_KEY"] = "test_search_key"
os.environ["AZURE_SEARCH_INDEX"] = "test_index"

# Patch before importing
with patch('openai.AzureOpenAI') as mock_azure_openai:
    mock_client = MagicMock()
    mock_azure_openai.return_value = mock_client
    from api.main import app

client = TestClient(app)

@patch('api.main.tts_generator.synthesize_speech')
def test_chat_endpoint(mock_tts):
    mock_tts.return_value = b"test_audio"
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test response"
    mock_client.chat.completions.create.return_value = mock_response

    response = client.post("/chat", json={"query": "What is Azure Functions?"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Test response"
