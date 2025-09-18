
# GenAI-RAG-App

This project demonstrates an end-to-end generative AI chatbot pipeline with Retrieval-Augmented Generation (RAG) and text-to-speech (TTS), deployed serverlessly on Azure Functions. The app acts as a "PSI 20 expert," using RAG on the companies' latest annual reports to answer questions about them. It leverages Azure AI Search for document retrieval, GPT-4o-mini-tts for generation and TTS, and FastAPI for API endpoints. The front-end provides a simple chat interface with TTS playback.

## Project Overview

- **Objective**: Build and deploy a generative AI chatbot that answers questions using RAG and provides spoken responses.
- **Dataset**: Annual reports from PSI 20 companies (not included in repo due to size).
- **Models**: GPT-4.1-mini for LLM, GPT-4o-mini-tts for TTS, and text-embedding-3-small for embeddings, integrated with Azure AI Search.
- **Platform**: Azure Functions for serverless deployment, Azure AI Foundry for base model deployments, FastAPI for API, Azure AI Search for retrieval.

## Repository Structure
```
retriever/         # Azure AI Search logic and LLM response generation (GPT-4.1-mini)
generator/         # TTS audio synthesis modules (GPT-4o-mini-tts)
api/               # FastAPI endpoints, Azure Functions triggers
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

- **Azure Functions Workflow** (`.github/workflows/deploy-functions.yml`):
  - Triggers on push to `main` branch or manual dispatch
  - Builds and deploys the Python API to Azure Functions
  - Requires `AZUREAPPSERVICE_PUBLISHPROFILE` secret

- **Azure Static Web Apps Workflow** (`.github/workflows/deploy-static-web-app.yml`):
  - Triggers on push to `main` branch or manual dispatch
  - Builds and deploys the frontend to Azure Static Web Apps
  - Requires `AZURE_STATIC_WEB_APPS_API_TOKEN` secret

### Deployment Steps

1. **Set up Azure Resources**:
   - Create an Azure Functions app
   - Create an Azure Static Web Apps resource
   - Configure CORS in Azure Functions to allow the Static Web Apps domain

2. **Configure GitHub Secrets**:
   - Get the publish profile from Azure Functions
   - Get the deployment token from Azure Static Web Apps
   - Add them as repository secrets

3. **Deploy**:
   - Push to the `main` branch to trigger automated deployment
   - Or manually trigger the workflows from the Actions tab

4. **Update Frontend URLs**:
   - After deployment, update the frontend to point to the Azure Functions API URL

## Pipeline Workflow

1. **User Query**: User submits a question via the front-end chat interface.
2. **Retrieval & Generation**: Retriever module uses GPT-4.1-mini with Azure AI Search RAG to find relevant document snippets and generate a contextual response.
3. **TTS Synthesis**: Generator module uses GPT-4o-mini-tts to synthesize speech audio (MP3) from the response text, returned as base64-encoded data.
4. **Response**: API returns both text and audio data to the front-end for display and playback.

## Dependencies

- **Python**: See `requirements.txt` for backend dependencies (FastAPI, openai, python-dotenv, uvicorn, pytest)
- **Node.js**: See `package.json` for front-end dependencies (minimal setup for static serving)

## Monitoring and Outputs

- **Azure Portal**: Monitor Azure Functions and AI Search usage, logs, and performance.
- **API Logs**: Check FastAPI logs for errors and request traces.
- **Front-end**: View chat and TTS playback in browser.

## Troubleshooting

- **Authentication Errors**: Verify environment variables and Azure credentials.
- **Search/Model Issues**: Ensure Azure AI Search index is populated and OpenAI credentials are valid.
- **TTS Audio Not Playing**: Check browser console for errors; ensure base64 audio data is being received.
- **Favicon 404 Errors**: These are normal and handled by returning 204 No Content to prevent repeated requests.
- **Deployment Errors**: Check Azure Functions logs and configuration.

## License

MIT License. See [LICENSE](LICENSE) for details.