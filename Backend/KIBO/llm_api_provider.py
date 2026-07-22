from google import genai
import os
from dotenv import load_dotenv, find_dotenv

# Central config — change provider/model here only
MODEL_NAME = "gemini-2.0-flash"

# Search upward for .env
load_dotenv(find_dotenv())
API_KEY = os.getenv("Gov_API_KEY") or os.getenv("GOV_API_KEY") or os.getenv("GEMINI_API_KEY")

_client = genai.Client(api_key=API_KEY)

def ask_ai(prompt: str) -> str:
    """
    Single entry point for all AI calls in the project.
    Swap the provider here later without touching any other file.
    """
    response = _client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text

def embed_text(text: str) -> list[float]:
    """
    Turns text into a vector (list of numbers) representing its meaning.
    Single entry point — swap provider here only.
    """
    result = _client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values


def ask_ai_stream(prompt: str):
    """
    Yields content chunks from Gemini LLM in real-time.
    """
    response = _client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=prompt
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text
