from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.notification_service import (
    NotificationServiceError,
    get_user_notifications,
    get_unread_notifications,
    mark_notification_read,
    mark_all_notifications_read,
    delete_notification,
    send_notification_to_user,
    broadcast_notification,
)
from app.utils.response import success_response, error_response
from app.utils.decorators import role_required


def _validate_notification_payload(data):
    errors = []
    title = (data.get("title") or "").strip()
    message = (data.get("message") or "").strip()

    if not title:
        errors.append("Title is required")
    if not message:
        errors.append("Message is required")

    return errors


@jwt_required()
def list_notifications_controller():
    identity = int(get_jwt_identity())

    notifications = get_user_notifications(identity)

    return success_response(
        "Notifications fetched successfully",
        data=[n.to_dict() for n in notifications],
    )


@jwt_required()
def list_unread_notifications_controller():
    identity = int(get_jwt_identity())

    notifications = get_unread_notifications(identity)

    return success_response(
        "Unread notifications fetched successfully",
        data=[n.to_dict() for n in notifications],
    )


@jwt_required()
def mark_notification_read_controller(notification_id):
    identity = int(get_jwt_identity())

    try:
        notification = mark_notification_read(notification_id, identity)
    except NotificationServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong updating the notification", status_code=500)

    return success_response("Notification marked as read", data=notification.to_dict())


@jwt_required()
def mark_all_notifications_read_controller():
    identity = int(get_jwt_identity())

    try:
        updated_count = mark_all_notifications_read(identity)
    except Exception:
        return error_response("Something went wrong updating notifications", status_code=500)

    return success_response(
        "All notifications marked as read", data={"updated_count": updated_count}
    )


@jwt_required()
def delete_notification_controller(notification_id):
    identity = int(get_jwt_identity())

    try:
        delete_notification(notification_id, identity, is_admin=False)
    except NotificationServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong deleting the notification", status_code=500)

    return success_response("Notification deleted successfully", data={})


@role_required("admin")
def send_notification_to_user_controller(user_id):
    data = request.get_json(silent=True) or {}

    errors = _validate_notification_payload(data)
    if errors:
        return error_response("Validation failed", errors, status_code=422)

    try:
        notification = send_notification_to_user(
            user_id, data.get("title").strip(), data.get("message").strip()
        )
    except NotificationServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong sending the notification", status_code=500)

    return success_response(
        "Notification sent successfully", data=notification.to_dict(), status_code=201
    )


@role_required("admin")
def broadcast_notification_controller():
    data = request.get_json(silent=True) or {}

    errors = _validate_notification_payload(data)
    if errors:
        return error_response("Validation failed", errors, status_code=422)

    try:
        sent_count = broadcast_notification(data.get("title").strip(), data.get("message").strip())
    except Exception:
        return error_response("Something went wrong broadcasting the notification", status_code=500)

    return success_response(
        "Notification broadcast successfully", data={"sent_count": sent_count}, status_code=201
    )


@role_required("admin")
def admin_delete_notification_controller(notification_id):
    try:
        delete_notification(notification_id, None, is_admin=True)
    except NotificationServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong deleting the notification", status_code=500)

    return success_response("Notification deleted successfully", data={})
