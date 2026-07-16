import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

Gov_API_KEY =os.getenv("Gov_API_KEY")

def format_docs(docs):
    """Combine the content of retrieved documents into a single text block."""
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(retriever):
    """Build and return the complete RAG query pipeline."""
    
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=Gov_API_KEY,
        temperature=0.2
    )


    template = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 

Context:
{context}

Question: {question}

Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)

   
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain