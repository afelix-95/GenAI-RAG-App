"""
Generator module for LLM and TTS integration.
- Uses GPT-4o-mini-tts via Azure OpenAI SDK
- Encapsulates text-to-speech
"""
import os
import base64
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2025-03-01-preview"
)

def synthesize_speech(text):
    with client.audio.speech.with_streaming_response.create(
        model=os.getenv("TTS_MODEL_NAME"),
        voice="coral",
        input=text,
        instructions="Speak in a cheerful and positive tone.",
    ) as response:
        audio_data = b""
        for chunk in response.iter_bytes():
            audio_data += chunk
        return base64.b64encode(audio_data).decode('utf-8')
