import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
try:
    from pydantic.types import SecretStr
except Exception:
    from pydantic import SecretStr

_raw_key = os.getenv("Gov_API_KEY")
Gov_API_KEY = SecretStr(_raw_key) if _raw_key is not None else None
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "documents"

def get_retriever():
    """Load the existing vector store and return it as a retriever."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        api_key= Gov_API_KEY
    )
    
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    
    return vectorstore.as_retriever(search_kwargs={"k": 3})