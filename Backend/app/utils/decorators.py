from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt

from app.utils.response import error_response


def role_required(*allowed_roles):
    """Restrict a route to callers whose JWT 'role' claim is in allowed_roles."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in allowed_roles:
                return error_response("You do not have permission to access this resource", status_code=403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
