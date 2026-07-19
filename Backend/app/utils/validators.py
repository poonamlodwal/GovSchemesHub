import re
from datetime import datetime


def validate_registration_payload(data):
    errors = []

    full_name = (data.get("full_name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    password = data.get("password") or ""
    confirm_password = data.get("confirm_password") or ""
    state = (data.get("state") or "").strip()
    district = (data.get("district") or "").strip()
    city = (data.get("city") or "").strip()
    gender = (data.get("gender") or "").strip()
    date_of_birth = (data.get("date_of_birth") or "").strip()
    occupation = (data.get("occupation") or "").strip()
    annual_income = data.get("annual_income")
    category = (data.get("category") or "").strip()

    if not full_name:
        errors.append("Full name is required")
    elif len(full_name) < 3:
        errors.append("Full name must be at least 3 characters")

    if not email:
        errors.append("Email is required")
    elif not re.match(r"^[\w\.\-]+@[\w\-]+\.[a-zA-Z]{2,}$", email):
        errors.append("Invalid email format")

    if not phone:
        errors.append("Phone number is required")
    elif not re.match(r"^[6-9]\d{9}$", phone):
        errors.append("Invalid phone number format")

    if not password:
        errors.append("Password is required")
    elif len(password) < 8:
        errors.append("Password must be at least 8 characters")

    if not confirm_password:
        errors.append("Confirm password is required")
    elif password and confirm_password != password:
        errors.append("Password and confirm password do not match")

    if not state:
        errors.append("State is required")

    if not district:
        errors.append("District is required")

    if not city:
        errors.append("City is required")

    if not gender:
        errors.append("Gender is required")
    elif gender.lower() not in ("male", "female", "other"):
        errors.append("Gender must be male, female, or other")

    if not date_of_birth:
        errors.append("Date of birth is required")
    else:
        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            errors.append("Date of birth must be in YYYY-MM-DD format")

    if not occupation:
        errors.append("Occupation is required")

    if annual_income in (None, ""):
        errors.append("Annual income is required")
    else:
        try:
            if float(annual_income) < 0:
                errors.append("Annual income must be a positive number")
        except (TypeError, ValueError):
            errors.append("Annual income must be a number")

    if not category:
        errors.append("Category is required")

    return errors


def validate_login_payload(data):
    errors = []

    identifier = (data.get("email") or data.get("phone") or "").strip()
    password = data.get("password") or ""

    if not identifier:
        errors.append("Email or phone is required")

    if not password:
        errors.append("Password is required")

    return errors


def validate_scheme_payload(data, partial=False):
    errors = []
    data = data or {}

    if not partial or "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            errors.append("Title is required")
        elif len(title) < 3:
            errors.append("Title must be at least 3 characters")

    if not partial or "category_id" in data:
        category_id = data.get("category_id")
        if category_id in (None, ""):
            errors.append("Category is required")
        else:
            try:
                int(category_id)
            except (TypeError, ValueError):
                errors.append("Category id must be a valid integer")

    if data.get("official_link"):
        if not re.match(r"^https?://", data.get("official_link")):
            errors.append("Official link must be a valid URL")

    if data.get("last_date"):
        try:
            datetime.strptime(data.get("last_date"), "%Y-%m-%d")
        except ValueError:
            errors.append("Last date must be in YYYY-MM-DD format")

    return errors


def allowed_file(filename, allowed_extensions):
    if not filename or "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in allowed_extensions


ALLOWED_DOCUMENT_TYPES = {
    "Aadhaar Card",
    "Income Certificate",
    "Caste Certificate",
    "Disability Certificate",
    "Domicile Certificate",
    "Other Supporting Documents",
}

ALLOWED_DOCUMENT_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
MAX_DOCUMENT_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def validate_document_upload(file, document_name, file_size=None):
    errors = []

    if file is None or not getattr(file, "filename", ""):
        errors.append("File is required")
    else:
        if not allowed_file(file.filename, ALLOWED_DOCUMENT_EXTENSIONS):
            errors.append("Only pdf, png, jpg, and jpeg files are allowed")

        if file_size is not None and file_size > MAX_DOCUMENT_SIZE_BYTES:
            errors.append("File size must not exceed 5 MB")

    document_name = (document_name or "").strip()
    if not document_name:
        errors.append("Document name is required")
    elif document_name not in ALLOWED_DOCUMENT_TYPES:
        errors.append(
            "Document name must be one of: " + ", ".join(sorted(ALLOWED_DOCUMENT_TYPES))
        )

    return errors
