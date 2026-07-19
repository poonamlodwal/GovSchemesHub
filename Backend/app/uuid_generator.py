import uuid


def generate_uuid():
    """Return a new UUID4 string. Used as default for public_id columns."""
    return str(uuid.uuid4())


def generate_scheme_code(prefix="SCH"):
    """Generate a short, human-readable scheme code, e.g. SCH-8F3A2B1C."""
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


def generate_session_id():
    """Generate a session ID for chat/auth sessions."""
    return str(uuid.uuid4())


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, AttributeError, TypeError):
        return False
