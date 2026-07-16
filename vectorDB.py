import os
try:
    from pydantic.types import SecretStr
except Exception:
    from pydantic import SecretStr

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

_raw_key = os.getenv("Gov_API_KEY")
Gov_API_KEY = SecretStr(_raw_key) if _raw_key is not None else None
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "documents"
 

def initialize_embeddings():
    """Initialize Google Generative AI Embeddings"""
    try:
        
        
        embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            api_key=Gov_API_KEY
        )
        print(" Embeddings initialized successfully")
        return embeddings
    except Exception as e:
        print(f"Error initializing embeddings: {e}")
        raise


def vector_store(embeddings):
    """Create or load Chroma vector database"""
    try:
        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        print(f"Vector database loaded/created at: {CHROMA_DB_PATH}")
        return vectorstore
    except Exception as e:
        print(f"Error creating vector database: {e}")
        raise
