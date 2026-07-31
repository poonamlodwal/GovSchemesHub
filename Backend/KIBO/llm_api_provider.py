from google import genai
import os
from dotenv import load_dotenv, find_dotenv

# Search upward for .env
load_dotenv(find_dotenv())

def get_api_key():
    return (
        os.getenv("Gov_API_KEY")
        or os.getenv("GOV_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )

def get_client():
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Backend missing GEMINI_API_KEY or GOV_API_KEY environment variable. Please set it in Render Dashboard -> Environment.")
    return genai.Client(api_key=api_key)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

def ask_ai(prompt: str) -> str:
    client = get_client()
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text

def embed_text(text: str) -> list[float]:
    client = get_client()
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return result.embeddings[0].values

def ask_ai_stream(prompt: str):
    client = get_client()
    try:
        response = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=prompt
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception:
        response = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=prompt
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
