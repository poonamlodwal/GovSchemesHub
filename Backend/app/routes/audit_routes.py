from flask import Blueprint

from app.controllers.audit_controller import (
    list_audit_logs_controller,
    get_audit_log_controller,
    get_audit_logs_by_user_controller,
    get_audit_logs_by_action_controller,
    get_latest_audit_logs_controller,
)

audit_bp = Blueprint("audit", __name__)

audit_bp.add_url_rule("", view_func=list_audit_logs_controller, methods=["GET"])
audit_bp.add_url_rule("/latest", view_func=get_latest_audit_logs_controller, methods=["GET"])
audit_bp.add_url_rule(
    "/user/<int:user_id>", view_func=get_audit_logs_by_user_controller, methods=["GET"]
)
audit_bp.add_url_rule(
    "/action/<string:action>", view_func=get_audit_logs_by_action_controller, methods=["GET"]
)
audit_bp.add_url_rule("/<int:log_id>", view_func=get_audit_log_controller, methods=["GET"])
