from flask import Blueprint

from app.controllers.notification_controller import (
    list_notifications_controller,
    list_unread_notifications_controller,
    mark_notification_read_controller,
    mark_all_notifications_read_controller,
    delete_notification_controller,
    send_notification_to_user_controller,
    broadcast_notification_controller,
    admin_delete_notification_controller,
)

notification_bp = Blueprint("notifications", __name__)

notification_bp.add_url_rule("", view_func=list_notifications_controller, methods=["GET"])
notification_bp.add_url_rule(
    "/unread", view_func=list_unread_notifications_controller, methods=["GET"]
)
notification_bp.add_url_rule(
    "/<int:notification_id>/read", view_func=mark_notification_read_controller, methods=["PATCH"]
)
notification_bp.add_url_rule(
    "/read-all", view_func=mark_all_notifications_read_controller, methods=["PATCH"]
)
notification_bp.add_url_rule(
    "/<int:notification_id>", view_func=delete_notification_controller, methods=["DELETE"]
)


admin_notification_bp = Blueprint("admin_notifications", __name__)

admin_notification_bp.add_url_rule(
    "/user/<int:user_id>", view_func=send_notification_to_user_controller, methods=["POST"]
)
admin_notification_bp.add_url_rule(
    "/broadcast", view_func=broadcast_notification_controller, methods=["POST"]
)
admin_notification_bp.add_url_rule(
    "/<int:notification_id>", view_func=admin_delete_notification_controller, methods=["DELETE"]
)
