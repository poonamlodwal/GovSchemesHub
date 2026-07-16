import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

Gov_API_KEY =os.getenv("Gov_API_KEY")
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "documents"

def get_retriever():
    """Load the existing vector store and return it as a retriever."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=Gov_API_KEY
    )
    
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    
    return vectorstore.as_retriever(search_kwargs={"k": 3})