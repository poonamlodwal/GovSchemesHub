from flask import Blueprint

from app.controllers.dashboard_controller import (
    get_dashboard_summary_controller,
    get_statistics_controller,
    get_recent_users_controller,
    get_recent_documents_controller,
    get_recent_notifications_controller,
)

dashboard_bp = Blueprint("dashboard", __name__)

dashboard_bp.add_url_rule("", view_func=get_dashboard_summary_controller, methods=["GET"])
dashboard_bp.add_url_rule(
    "/statistics", view_func=get_statistics_controller, methods=["GET"]
)
dashboard_bp.add_url_rule(
    "/recent-users", view_func=get_recent_users_controller, methods=["GET"]
)
dashboard_bp.add_url_rule(
    "/recent-documents", view_func=get_recent_documents_controller, methods=["GET"]
)
dashboard_bp.add_url_rule(
    "/recent-notifications", view_func=get_recent_notifications_controller, methods=["GET"]
)
