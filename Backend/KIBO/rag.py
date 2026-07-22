from vector_store import search
from llm_api_provider import ask_ai

def ask_with_rag(question: str, n_results: int = 5, filter_document_type: str = None):
    try:
        chunks = search(question, n_results=n_results, filter_document_type=filter_document_type)
    except Exception as e:
        return f"Error querying vector store: {str(e)}"

    if not chunks:
        return "No relevant information found in the documents."

    context_blocks = []
    for i, c in enumerate(chunks):
        metadata = c.get("metadata", {})
        doc_type = metadata.get("document_type") or metadata.get("doc_type") or "Scheme"
        filename = metadata.get("filename") or "Document"
        context_blocks.append(
            f"[Source {i+1}: {doc_type} — {filename}]\n{c.get('text', '')}"
        )
    context = "\n\n".join(context_blocks)

    prompt = f"""You are an AI assistant for Indian Government Schemes. Answer the question using ONLY the context below. If the answer isn't in the context, say so clearly. Cite which source(s) you used by number.

CONTEXT:
{context}

QUESTION: {question}

ANSWER (cite sources like [Source 1], [Source 2]):"""

    try:
        return ask_ai(prompt)
    except Exception as e:
        return f"Error calling AI Assistant: {str(e)}"


def ask_with_rag_stream(question: str, n_results: int = 5, filter_document_type: str = None, history: list = None):

    try:
        chunks = search(question, n_results=n_results, filter_document_type=filter_document_type)
    except Exception as e:
        yield {"error": f"Error querying vector store: {str(e)}"}
        return

    sources = []
    context_blocks = []
    for i, c in enumerate(chunks):
        metadata = c.get("metadata", {})
        doc_type = metadata.get("document_type") or metadata.get("doc_type") or "Scheme"
        filename = metadata.get("filename") or "Document"
        sources.append({
            "id": i + 1,
            "filename": filename,
            "doc_type": doc_type
        })
        context_blocks.append(
            f"[Source {i+1}: {doc_type} — {filename}]\n{c.get('text', '')}"
        )

    if not chunks:
        yield {"sources":[]}
        yield {"text": "No relevant information found in the documents."}
        return
    
    yield {"sources": sources}
context = "\n\n".join(context_blocks)

history_text = ""
if history:
    for msg in history:
        role = "User" if msg.get("role") == "user" else "Assistant"
        history_text += f"\n{role}: {msg.get('content', '')}"

prompt = f"""You are an AI assistant for Indian Government Schemes. Answer the question using ONLY the context below. If the answer isn't in the context, say so clearly. Cite which source(s) you used by number.
CONVERSATION HISTORY (for context):
{history_text if history_text else "No previous conversation."}

CONTEXT:
{context}

CURRENT QUESTION: {question}

ANSWER (cite sources like [Source 1], [Source 2]):"""

try:
    from llm_api_provider import ask_ai_stream
    for token in ask_ai_stream(prompt):
        if token:
         yield {"text": token}
except Exception as e:
         yield {"error": f"Error calling AI Assistant: {str(e)}"}


if __name__ == "__main__":
    question = "What is the eligibility criteria for the PM-KISAN scheme?"
    answer = ask_with_rag(question)
    print(answer)

