from flask import request

from app.services.scheme_service import (
    SchemeServiceError,
    create_scheme,
    update_scheme,
    delete_scheme,
    get_scheme_by_id,
    list_schemes,
    list_schemes_by_category,
    list_schemes_by_state,
    list_categories,
)
from app.utils.validators import validate_scheme_payload
from app.utils.response import success_response, error_response
from app.utils.decorators import role_required


@role_required("admin")
def create_scheme_controller():
    data = request.get_json(silent=True) or {}

    errors = validate_scheme_payload(data, partial=False)
    if errors:
        return error_response("Validation failed", errors, status_code=422)

    try:
        scheme = create_scheme(data)
    except SchemeServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong creating the scheme", status_code=500)

    return success_response("Scheme created successfully", data=scheme.to_dict(), status_code=201)


def list_schemes_controller():
    try:
        pagination = list_schemes(request.args)
    except Exception:
        return error_response("Something went wrong fetching schemes", status_code=500)

    return success_response(
        "Schemes fetched successfully",
        data={
            "items": [scheme.to_dict() for scheme in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
    )


def get_scheme_controller(scheme_id):
    try:
        scheme = get_scheme_by_id(scheme_id)
    except SchemeServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)

    return success_response("Scheme fetched successfully", data=scheme.to_dict())


@role_required("admin")
def update_scheme_controller(scheme_id):
    data = request.get_json(silent=True) or {}

    errors = validate_scheme_payload(data, partial=True)
    if errors:
        return error_response("Validation failed", errors, status_code=422)

    try:
        scheme = update_scheme(scheme_id, data)
    except SchemeServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong updating the scheme", status_code=500)

    return success_response("Scheme updated successfully", data=scheme.to_dict())


@role_required("admin")
def delete_scheme_controller(scheme_id):
    try:
        delete_scheme(scheme_id)
    except SchemeServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)

    return success_response("Scheme deleted successfully", data={})


def list_categories_controller():
    categories = list_categories()
    return success_response(
        "Categories fetched successfully",
        data=[category.to_dict() for category in categories],
    )


def schemes_by_category_controller(category_id):
    try:
        schemes = list_schemes_by_category(category_id)
    except SchemeServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)

    return success_response(
        "Schemes fetched successfully", data=[scheme.to_dict() for scheme in schemes]
    )


def schemes_by_state_controller(state):
    schemes = list_schemes_by_state(state)
    return success_response(
        "Schemes fetched successfully", data=[scheme.to_dict() for scheme in schemes]
    )
