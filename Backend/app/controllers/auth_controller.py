from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from app.services.auth_service import (
    AuthServiceError,
    register_user,
    authenticate_user,
    get_current_user,
)
from app.utils.validators import (
    validate_registration_payload,
    validate_login_payload,
)
from app.utils.response import success_response, error_response
from app.utils.token_blocklist import add_token_to_blocklist


def register_controller():
    data = request.get_json(silent=True) or {}

    errors = validate_registration_payload(data)
    if errors:
        return error_response("Validation failed", errors, status_code=422)

    try:
        user = register_user(data)
    except AuthServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong during registration", status_code=500)

    return success_response(
        "User registered successfully", data=user.to_dict(), status_code=201
    )


def login_controller():
    data = request.get_json(silent=True) or {}

    errors = validate_login_payload(data)
    if errors:
        return error_response("Validation failed", errors, status_code=422)

    identifier = data.get("email") or data.get("phone")

    try:
        user = authenticate_user(identifier, data.get("password"))
    except AuthServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong during login", status_code=500)

    additional_claims = {"role": "user"}
    access_token = create_access_token(
        identity=str(user.id), additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=str(user.id), additional_claims=additional_claims
    )

    return success_response(
        "Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
        },
        status_code=200,
    )


@jwt_required(refresh=True)
def refresh_controller():
    identity = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role", "user")

    access_token = create_access_token(
        identity=identity, additional_claims={"role": role}
    )

    return success_response(
        "Access token refreshed successfully",
        data={"access_token": access_token},
        status_code=200,
    )


@jwt_required()
def me_controller():
    identity = get_jwt_identity()

    try:
        user = get_current_user(int(identity))
    except AuthServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong fetching the current user", status_code=500)

    return success_response("Current user fetched successfully", data=user.to_dict())


@jwt_required()
def logout_controller():
    jti = get_jwt()["jti"]
    add_token_to_blocklist(jti)

    return success_response("Logout successful", data={}, status_code=200)
