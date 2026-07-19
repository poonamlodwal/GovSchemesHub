from flask import Blueprint

from app.controllers.document_controller import (
    upload_document_controller,
    list_documents_controller,
    get_document_controller,
    delete_document_controller,
)

document_bp = Blueprint("documents", __name__)

document_bp.add_url_rule("/upload", view_func=upload_document_controller, methods=["POST"])
document_bp.add_url_rule("", view_func=list_documents_controller, methods=["GET"])
document_bp.add_url_rule("/<int:document_id>", view_func=get_document_controller, methods=["GET"])
document_bp.add_url_rule(
    "/<int:document_id>",
    view_func=delete_document_controller,
    methods=["DELETE"],
    endpoint="delete_document_controller",
)
