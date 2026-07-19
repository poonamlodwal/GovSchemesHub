from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from app.utils.responses import error_response


def roles_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            if role not in allowed_roles:
                return error_response(
                    "You do not have permission to perform this action.", 403
                )
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def register_jwt_callbacks(jwt_manager, db):
    from app.utils.token_blocklist import TokenBlocklist

    @jwt_manager.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None

    @jwt_manager.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return error_response("The token has expired.", 401)

    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error_string):
        return error_response("Invalid token. Please log in again.", 401)

    @jwt_manager.unauthorized_loader
    def missing_token_callback(error_string):
        return error_response("Missing authorization token.", 401)

    @jwt_manager.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return error_response("This token has been revoked.", 401)
