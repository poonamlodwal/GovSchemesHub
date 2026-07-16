import os
from dotenv import load_dotenv
from document_loader import load_my_documents
from chunks import splits_documents
from vectorDB import vector_store
from retriever import get_retriever
from llm_chain import get_rag_chain

def main():
    print("--- Starting RAG Pipeline ---")

    # 1. Load all raw files
    docs_path = "./docs"
    documents = load_my_documents(docs_path)

    # 2. Split documents into small chunks
    chunks = splits_documents(documents)

    # 3. Embed text and save to Chroma DB
    vectorstore = vector_store(chunks)

    # 4. Initialize Retriever and LLM Chain
    retriever = get_retriever()
    rag_chain = get_rag_chain(retriever)

    # 5. Run a test query
    query = "What is the summary of the documents?" 
    print(f"\nUser Query: {query}")
    print("Generating response...")
    
    response = rag_chain.invoke(query)
    
    print("\n--- LLM Response ---")
    print(response)
    print("--------------------")

if __name__ == "__main__":
    main()