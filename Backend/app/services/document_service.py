import os

from app.models.uploaded_document import UploadedDocument
from app.utils.file_handler import save_uploaded_file, delete_file_from_disk


class DocumentServiceError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


def upload_document(user_id, file_storage, document_name, upload_folder):
    unique_filename, absolute_path, relative_path, file_size = save_uploaded_file(
        file_storage, upload_folder
    )

    document = UploadedDocument(
        user_id=user_id,
        document_name=document_name,
        file_path=relative_path,
    )
    document.save()

    return document


def list_documents(requester_id, requester_role, filter_user_id=None):
    query = UploadedDocument.active_query()

    if requester_role == "admin":
        if filter_user_id:
            query = query.filter(UploadedDocument.user_id == int(filter_user_id))
    else:
        query = query.filter(UploadedDocument.user_id == requester_id)

    return query.order_by(UploadedDocument.uploaded_at.desc()).all()


def _get_owned_document(document_id, requester_id, requester_role):
    document = UploadedDocument.get_by_id(document_id)
    if not document or document.is_deleted:
        raise DocumentServiceError("Document not found", status_code=404)

    if requester_role != "admin" and document.user_id != requester_id:
        raise DocumentServiceError(
            "You do not have permission to access this document", status_code=403
        )

    return document


def get_document(document_id, requester_id, requester_role):
    return _get_owned_document(document_id, requester_id, requester_role)


def delete_document(document_id, requester_id, requester_role, upload_folder):
    document = _get_owned_document(document_id, requester_id, requester_role)

    filename = os.path.basename(document.file_path)
    absolute_path = os.path.join(upload_folder, filename)
    delete_file_from_disk(absolute_path)

    document.delete()
    return document
