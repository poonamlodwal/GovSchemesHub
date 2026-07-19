from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.services.document_service import (
    DocumentServiceError,
    upload_document,
    list_documents,
    get_document,
    delete_document,
)
from app.utils.file_handler import get_file_size
from app.utils.validators import validate_document_upload
from app.utils.response import success_response, error_response


@jwt_required()
def upload_document_controller():
    identity = int(get_jwt_identity())

    file = request.files.get("file")
    document_name = request.form.get("document_name")

    file_size = get_file_size(file) if file else None

    errors = validate_document_upload(file, document_name, file_size=file_size)
    if errors:
        return error_response("Validation failed", errors, status_code=422)

    try:
        document = upload_document(
            identity, file, document_name.strip(), current_app.config["UPLOAD_FOLDER"]
        )
    except DocumentServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong uploading the document", status_code=500)

    return success_response(
        "Document uploaded successfully", data=document.to_dict(), status_code=201
    )


@jwt_required()
def list_documents_controller():
    identity = int(get_jwt_identity())
    role = get_jwt().get("role", "user")

    filter_user_id = request.args.get("user_id")

    try:
        documents = list_documents(identity, role, filter_user_id=filter_user_id)
    except Exception:
        return error_response("Something went wrong fetching documents", status_code=500)

    return success_response(
        "Documents fetched successfully",
        data=[document.to_dict() for document in documents],
    )


@jwt_required()
def get_document_controller(document_id):
    identity = int(get_jwt_identity())
    role = get_jwt().get("role", "user")

    try:
        document = get_document(document_id, identity, role)
    except DocumentServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)

    return success_response("Document fetched successfully", data=document.to_dict())


@jwt_required()
def delete_document_controller(document_id):
    identity = int(get_jwt_identity())
    role = get_jwt().get("role", "user")

    try:
        delete_document(document_id, identity, role, current_app.config["UPLOAD_FOLDER"])
    except DocumentServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong deleting the document", status_code=500)

    return success_response("Document deleted successfully", data={})
