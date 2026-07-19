from app.models.chat_history import ChatHistory


class ChatServiceError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


def get_rag_response(question):
    """
    Placeholder call site for the AI/RAG module (Google Gemini + ChromaDB
    retrieval), owned by another team. Intentionally NOT implemented here.
    The RAG team will replace this function's body with the real
    implementation; the signature (question -> answer string) must stay
    the same so chat_service/chat_controller need no further changes.
    """
    raise NotImplementedError(
        "get_rag_response() is a placeholder; the AI/RAG module will provide the real implementation"
    )


def process_chat_message(user_id, question):
    question = (question or "").strip()
    if not question:
        raise ChatServiceError("Question is required", status_code=422)

    answer = get_rag_response(question)

    chat_entry = ChatHistory(
        user_id=user_id,
        question=question,
        answer=answer,
    )
    chat_entry.save()

    return chat_entry


def get_chat_history(user_id):
    return (
        ChatHistory.active_query()
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .all()
    )


def delete_chat_history(user_id):
    entries = ChatHistory.active_query().filter(ChatHistory.user_id == user_id).all()
    deleted_count = len(entries)
    for entry in entries:
        entry.delete()
    return deleted_count
