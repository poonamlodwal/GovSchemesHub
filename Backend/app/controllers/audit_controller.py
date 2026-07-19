from flask import request

from app.services.audit_service import (
    AuditServiceError,
    get_all_logs,
    get_log_by_id,
    get_logs_by_user,
    get_logs_by_action,
    get_latest_logs,
)
from app.utils.response import success_response, error_response
from app.utils.decorators import role_required


@role_required("admin")
def list_audit_logs_controller():
    try:
        result = get_all_logs(request.args)
    except Exception:
        return error_response("Something went wrong fetching audit logs", status_code=500)

    return success_response("Audit logs fetched successfully", data=result)


@role_required("admin")
def get_audit_log_controller(log_id):
    try:
        log = get_log_by_id(log_id)
    except AuditServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)

    return success_response("Audit log fetched successfully", data=log.to_dict())


@role_required("admin")
def get_audit_logs_by_user_controller(user_id):
    try:
        result = get_logs_by_user(user_id, request.args)
    except Exception:
        return error_response("Something went wrong fetching audit logs", status_code=500)

    return success_response("Audit logs fetched successfully", data=result)


@role_required("admin")
def get_audit_logs_by_action_controller(action):
    try:
        result = get_logs_by_action(action, request.args)
    except Exception:
        return error_response("Something went wrong fetching audit logs", status_code=500)

    return success_response("Audit logs fetched successfully", data=result)


@role_required("admin")
def get_latest_audit_logs_controller():
    limit = request.args.get("limit", 10)

    try:
        limit = int(limit)
    except (TypeError, ValueError):
        return error_response("Validation failed", ["limit must be an integer"], status_code=422)

    try:
        logs = get_latest_logs(limit=limit)
    except Exception:
        return error_response("Something went wrong fetching latest audit logs", status_code=500)

    return success_response("Latest audit logs fetched successfully", data=logs)
