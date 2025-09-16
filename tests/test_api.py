import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/chat", json={"query": "What is Azure Functions?"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
