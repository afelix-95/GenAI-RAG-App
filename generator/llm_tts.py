"""
Generator module for LLM and TTS integration.
- Uses GPT-4o-mini-tts via Azure OpenAI SDK
- Encapsulates both text generation and text-to-speech
"""
import os
import openai

OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
TTS_MODEL_NAME = os.getenv("TTS_MODEL_NAME", "GPT-4o-mini-tts")

openai.api_type = "azure"
openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_ENDPOINT
openai.api_version = "2023-05-15"

class LLM_TTS_Generator:
    def __init__(self):
        self.deployment = OPENAI_DEPLOYMENT
        self.tts_model = TTS_MODEL_NAME

    def generate_response(self, prompt):
        response = openai.ChatCompletion.create(
            engine=self.deployment,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512
        )
        return response["choices"][0]["message"]["content"]

    def synthesize_speech(self, text):
        # Placeholder for TTS API call (Azure OpenAI Speech or similar)
        # Return audio bytes or file path
        return b"AUDIO_DATA"  # Replace with actual TTS integration
