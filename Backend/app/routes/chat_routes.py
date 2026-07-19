from flask import Blueprint

from app.controllers.chat_controller import (
    send_chat_message_controller,
    get_chat_history_controller,
    delete_chat_history_controller,
)

chat_bp = Blueprint("chat", __name__)

chat_bp.add_url_rule("", view_func=send_chat_message_controller, methods=["POST"])
chat_bp.add_url_rule("/history", view_func=get_chat_history_controller, methods=["GET"])
chat_bp.add_url_rule(
    "/history",
    view_func=delete_chat_history_controller,
    methods=["DELETE"],
    endpoint="delete_chat_history_controller",
)
