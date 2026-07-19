from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.chat_service import (
    ChatServiceError,
    process_chat_message,
    get_chat_history,
    delete_chat_history,
)
from app.utils.response import success_response, error_response


@jwt_required()
def send_chat_message_controller():
    identity = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    question = data.get("question")

    try:
        chat_entry = process_chat_message(identity, question)
    except ChatServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except NotImplementedError:
        return error_response(
            "AI response service is not yet available", status_code=500
        )
    except Exception:
        return error_response("Something went wrong processing your message", status_code=500)

    return success_response(
        "Chat message processed successfully", data=chat_entry.to_dict(), status_code=201
    )


@jwt_required()
def get_chat_history_controller():
    identity = int(get_jwt_identity())

    try:
        history = get_chat_history(identity)
    except Exception:
        return error_response("Something went wrong fetching chat history", status_code=500)

    return success_response(
        "Chat history fetched successfully",
        data=[entry.to_dict() for entry in history],
    )


@jwt_required()
def delete_chat_history_controller():
    identity = int(get_jwt_identity())

    try:
        deleted_count = delete_chat_history(identity)
    except Exception:
        return error_response("Something went wrong deleting chat history", status_code=500)

    return success_response(
        "Chat history deleted successfully", data={"deleted_count": deleted_count}
    )
