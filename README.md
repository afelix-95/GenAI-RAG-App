
# GenAI-RAG-App

This project demonstrates an end-to-end generative AI chatbot pipeline with Retrieval-Augmented Generation (RAG) and text-to-speech (TTS), deployed serverlessly on Azure Functions. The app acts as a "PSI 20 expert," using RAG on the companies' latest annual reports to answer questions about them. It leverages Azure AI Search for document retrieval, GPT-4o-mini-tts for generation and TTS, and FastAPI for API endpoints. The front-end provides a simple chat interface with TTS playback.

## Project Overview

- **Objective**: Build and deploy a generative AI chatbot that answers questions using RAG and provides spoken responses.
- **Dataset**: Annual reports from PSI 20 companies (not included in repo due to size).
- **Models**: GPT-4.1-mini for LLM, GPT-4o-mini-tts for TTS, and text-embedding-3-small for embeddings, integrated with Azure AI Search.
- **Platform**: Azure Functions for serverless deployment, Azure AI Foundry for base model deployments, FastAPI for API, Azure AI Search for retrieval.

## Semantic Kernel Integration

This project leverages **Microsoft Semantic Kernel** (SK) to orchestrate the AI pipeline, providing a structured and extensible framework for integrating multiple AI services.

### Key Components

- **Kernel Setup** (`api/semantic_kernel_setup.py`): Initializes the SK kernel with Azure OpenAI service integration
- **RAG Plugin** (`RAGPlugin` class): Custom plugin containing kernel functions for RAG and TTS operations
- **Kernel Functions**: Decorated methods that can be invoked by the kernel:
  - `ProcessRAGQuery`: Handles document retrieval and response generation using Azure AI Search
  - `TextToSpeech`: Converts generated text responses to audio using Azure OpenAI TTS

### Orchestration Flow

1. **Kernel Initialization**: Azure OpenAI service is registered with the kernel
2. **Plugin Registration**: RAGPlugin is added to the kernel with defined functions
3. **Query Processing**: User queries are processed through kernel invocation:
   - RAG function retrieves relevant documents and generates contextual responses
   - TTS function synthesizes audio from the text response
4. **Response Assembly**: Kernel returns structured output with both text and audio data

### Benefits

- **Modularity**: Clean separation of AI operations through plugins and functions
- **Extensibility**: Easy to add new AI capabilities or modify existing ones
- **Type Safety**: KernelArguments provide structured parameter passing
- **Async Support**: Native support for asynchronous operations in the pipeline

## Repository Structure
```
retriever/         # Azure AI Search logic and LLM response generation (GPT-4.1-mini)
generator/         # TTS audio synthesis modules (GPT-4o-mini-tts)
api/               # FastAPI endpoints, Azure Functions triggers, Semantic Kernel orchestration
frontend/          # Chatbot UI, TTS playback
tests/             # Unit tests, demo scripts
.env.example       # Example config
requirements.txt   # Python dependencies
package.json       # Front-end dependencies
```

## Prerequisites

- **Azure Subscription**: Active Azure account with access to Azure AI Services, Azure AI Search and Azure Functions.
- **GitHub Repository**: Fork or clone this repository.
- **Secrets**:
  - `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_API_KEY`, `AZURE_SEARCH_INDEX`
  - `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `TTS_MODEL_NAME`
  - `EMBEDDING_MODEL_NAME`
- **Tools**:
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
	- **Azure Functions (API)**: The API is configured for Azure Functions deployment. Use the GitHub Actions workflow in `.github/workflows/deploy-functions.yml` for automated deployment.
	- **Azure Static Web Apps (Frontend)**: The frontend can be deployed separately to Azure Static Web Apps using the workflow in `.github/workflows/deploy-static-web-app.yml`.
	- **Manual Deployment**: Use Azure CLI or Azure Portal to deploy the Azure Functions app.
	- **Secrets Setup**: In your GitHub repository, add the following secrets:
		- `AZUREAPPSERVICE_PUBLISHPROFILE`: Azure Functions publish profile
		- `AZURE_STATIC_WEB_APPS_API_TOKEN`: Azure Static Web Apps deployment token

## CI/CD and Deployment

This project uses GitHub Actions for automated deployment to Azure:

- **Azure Functions (API Backend)**: Successfully deployed to `psi20expertapp` in Canada Central region
- **Workflow**: `.github/workflows/main_psi20expertapp.yml` handles build and deployment
- **Deployment Method**: Uses Azure CLI zip deployment

### Deployment Steps

1. **Set up Azure Resources**:
   - Azure Functions app
   - Azure AI Search service
   - Azure OpenAI service with deployments for (recommended):
     - `gpt-4.1-mini` (chat completions)
     - `gpt-4o-mini-tts` (text-to-speech)
     - `text-embedding-3-small` (embeddings)

2. **Configure Environment Variables in Azure**:
   ```bash
   az functionapp config appsettings set --name your-app-name --resource-group your-resource-group --settings \
     AZURE_SEARCH_ENDPOINT="your-search-endpoint" \
     AZURE_SEARCH_API_KEY="your-search-key" \
     AZURE_SEARCH_INDEX="your-index-name" \
     AZURE_OPENAI_API_KEY="your-openai-key" \
     AZURE_OPENAI_ENDPOINT="your-openai-endpoint" \
     CHAT_MODEL_NAME="your-llm-model" \
     TTS_MODEL_NAME="your-tts-model" \
     EMBEDDING_MODEL_NAME="your-embedding-model"
   ```

3. **Deploy**:
   - Push to `main` branch to trigger automated deployment
   - Or run: `az functionapp deployment source config-zip --name psi20expertapp --resource-group psi20expertapp_group --src .`

4. **Access the Application**:
   - Frontend: `https://psi20expertapp-g4b4b0dnceebf0fk.canadacentral-01.azurewebsites.net/`
   - API: `https://psi20expertapp-g4b4b0dnceebf0fk.canadacentral-01.azurewebsites.net/chat`

## Pipeline Workflow

The application uses **Microsoft Semantic Kernel** to orchestrate the end-to-end AI pipeline:

1. **User Query**: User submits a question via the front-end chat interface.
2. **Semantic Kernel Orchestration**:
   - Kernel invokes `RAGPlugin.ProcessRAGQuery` to retrieve relevant document snippets from Azure AI Search and generate contextual responses using GPT-4.1-mini
   - Kernel invokes `RAGPlugin.TextToSpeech` to synthesize speech audio (MP3) from the response text using GPT-4o-mini-tts
3. **Response**: API returns both text and base64-encoded audio data to the front-end for display and playback.

### Technical Implementation

- **Plugin Architecture**: Custom RAGPlugin encapsulates AI operations as kernel functions
- **Service Integration**: Azure OpenAI services are registered with the kernel for unified access
- **Async Processing**: All operations are handled asynchronously for optimal performance
- **Error Handling**: Kernel provides structured error handling and logging

## Dependencies

- **Python**: See `requirements.txt` for backend dependencies (FastAPI, openai, python-dotenv, uvicorn, pytest, semantic-kernel)
- **Node.js**: See `package.json` for front-end dependencies (minimal setup for static serving)

## Monitoring and Outputs

- **Azure Portal**: Monitor Azure Functions and AI Search usage, logs, and performance.
- **API Logs**: Check FastAPI logs for errors and request traces.
- **Front-end**: View chat and TTS playback in browser.

## Troubleshooting

- **Authentication Errors**: Verify environment variables and Azure credentials.
- **Search/Model Issues**: Ensure Azure AI Search index is populated and OpenAI credentials are valid.
- **TTS Audio Not Playing**: Check browser console for errors; ensure base64 audio data is being received.
- **Semantic Kernel Errors**: Check kernel initialization and plugin registration; verify Azure OpenAI service configuration.
- **Favicon 404 Errors**: These are normal and handled by returning 204 No Content to prevent repeated requests.
- **Deployment Errors**: Check Azure Functions logs and configuration.

## License

MIT License. See [LICENSE](LICENSE) for details.