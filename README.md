
# GenAI-RAG-App

This project demonstrates an end-to-end generative AI chatbot pipeline with Retrieval-Augmented Generation (RAG) and text-to-speech (TTS), deployed serverlessly on Azure Functions. It leverages Azure AI Search for document retrieval, GPT-4o-mini-tts for generation and TTS, and FastAPI for API endpoints. The front-end provides a simple chat interface with TTS playback.

## Project Overview

- **Objective**: Build and deploy a generative AI chatbot that answers questions using RAG and provides spoken responses.
- **Dataset**: Sample datasets (annual reports from PSI 20).
- **Model**: GPT-4o-mini-tts for LLM and TTS, integrated with Azure AI Search.
- **Platform**: Azure Functions for serverless deployment, FastAPI for API, Azure AI Search for retrieval.
- **Automation**: Deployment scripts and CI/CD (recommend GitHub Actions for future automation).

## Repository Structure
```
retriever/         # Azure AI Search logic
generator/         # LLM and TTS modules
api/               # FastAPI endpoints, Azure Functions triggers
frontend/          # Chatbot UI, TTS playback
data/              # Sample datasets
tests/             # Unit tests, demo scripts
.env.example       # Example config
requirements.txt   # Python dependencies
package.json       # Front-end dependencies
CHALLENGES.md      # Write-up on technical challenges
```

## Prerequisites

- **Azure Subscription**: Active Azure account with access to Azure AI Search and Azure Functions.
- **GitHub Repository**: Fork or clone this repository.
- **Secrets**:
  - `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_API_KEY`, `AZURE_SEARCH_INDEX`
  - `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `TTS_MODEL_NAME`
  - `EMBEDDING_MODEL_NAME`
- **Tools**:
  - Azure CLI
  - Python 3.10+
  - Node.js (for front-end)

## Setup Instructions

1. **Clone the Repository**:
	```bash
	git clone https://github.com/afelix-95/genai-rag-app.git
	cd genai-rag-app
	```

2. **Configure Azure Services**:
	- Set up Azure AI Search and Azure Functions resources.

3. **Set Up Environment Variables**:
	- Copy `.env.example` to `.env` and fill in credentials for Azure AI Search and OpenAI.

4. **Install Dependencies**:
	- Python: `pip install -r requirements.txt`
	- Front-end: `npm install` (if using React/JS)

5. **Run Locally**:
	- Start the API server: `uvicorn api.main:app --reload`
	- Open the front-end in your browser: `http://localhost:8000/` (served by the API)

6. **Deploy**:
	- Use Azure Functions deployment scripts (see documentation for details).

## Pipeline Workflow

1. **User Query**: User submits a question via the front-end.
2. **Retrieval**: Retriever module queries Azure AI Search for relevant documents.
3. **Generation**: Generator module (GPT-4o-mini-tts) creates a response using retrieved context.
4. **TTS**: Generator synthesizes speech from the response.
5. **Response**: API returns text and audio to the front-end for playback.

## Dependencies

- **Python**: See `requirements.txt` for backend dependencies (FastAPI, azure-search-documents, openai, python-dotenv, etc.)
- **Node.js**: See `package.json` for front-end dependencies.

## Monitoring and Outputs

- **Azure Portal**: Monitor Azure Functions and AI Search usage, logs, and performance.
- **API Logs**: Check FastAPI logs for errors and request traces.
- **Front-end**: View chat and TTS playback in browser.

## Troubleshooting

- **Authentication Errors**: Verify environment variables and Azure credentials.
- **Search/Model Issues**: Ensure Azure AI Search index is populated and OpenAI credentials are valid.
- **Deployment Errors**: Check Azure Functions logs and configuration.

## License

MIT License. See [LICENSE](LICENSE) for details.