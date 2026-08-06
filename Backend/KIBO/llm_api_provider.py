from google import genai
import os
import time
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

# Model fallback chain: try each model in order when quota is exceeded
MODEL_FALLBACK_CHAIN = [
    os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
]

def _is_quota_error(e: Exception) -> bool:
    """Check if the exception is a 429 quota exceeded error."""
    error_str = str(e)
    return "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower()

def ask_ai(prompt: str) -> str:
    client = get_client()
    last_error = None
    for model in MODEL_FALLBACK_CHAIN:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            last_error = e
            if _is_quota_error(e):
                # Quota exceeded on this model, try next in chain
                time.sleep(1)
                continue
            raise e
    raise last_error

def embed_text(text: str) -> list[float]:
    client = get_client()
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return result.embeddings[0].values

def ask_ai_stream(prompt: str):
    client = get_client()
    last_error = None
    for model in MODEL_FALLBACK_CHAIN:
        try:
            response = client.models.generate_content_stream(
                model=model,
                contents=prompt
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
            return  # success — stop trying fallbacks
        except Exception as e:
            last_error = e
            if _is_quota_error(e):
                # Quota exceeded on this model, try next in chain
                time.sleep(1)
                continue
            raise e
    # All models exhausted
    raise last_error
