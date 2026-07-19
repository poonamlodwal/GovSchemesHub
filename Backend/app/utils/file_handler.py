import os
import uuid

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def get_file_extension(filename):
    if not filename or "." not in filename:
        return ""
    return filename.rsplit(".", 1)[1].lower()


def is_extension_allowed(filename):
    return get_file_extension(filename) in ALLOWED_EXTENSIONS


def get_file_size(file_storage):
    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    return size


def generate_unique_filename(original_filename):
    safe_name = secure_filename(original_filename)
    extension = get_file_extension(safe_name)
    unique_name = f"{uuid.uuid4().hex}.{extension}" if extension else uuid.uuid4().hex
    return unique_name


def save_uploaded_file(file_storage, upload_folder):
    """
    Save the given Werkzeug FileStorage to upload_folder under a unique name.
    Returns (unique_filename, absolute_path, relative_path, file_size).
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)

    unique_filename = generate_unique_filename(file_storage.filename)
    absolute_path = os.path.join(upload_folder, unique_filename)

    file_storage.save(absolute_path)
    file_size = os.path.getsize(absolute_path)

    relative_path = os.path.join("uploads", unique_filename)

    return unique_filename, absolute_path, relative_path, file_size


def delete_file_from_disk(absolute_path):
    if absolute_path and os.path.exists(absolute_path):
        os.remove(absolute_path)
        return True
    return False
