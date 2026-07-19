from app.extensions import db
from app.models.notification import Notification
from app.models.user import User


class NotificationServiceError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


def _get_owned_notification(notification_id, user_id, is_admin=False):
    notification = Notification.get_by_id(notification_id)
    if not notification or notification.is_deleted:
        raise NotificationServiceError("Notification not found", status_code=404)

    if not is_admin and notification.user_id != user_id:
        raise NotificationServiceError(
            "You do not have permission to access this notification", status_code=403
        )

    return notification


def get_user_notifications(user_id):
    return (
        Notification.active_query()
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def get_unread_notifications(user_id):
    return (
        Notification.active_query()
        .filter(Notification.user_id == user_id, Notification.is_read.is_(False))
        .order_by(Notification.created_at.desc())
        .all()
    )


def mark_notification_read(notification_id, user_id):
    notification = _get_owned_notification(notification_id, user_id)
    notification.is_read = True
    db.session.commit()
    return notification


def mark_all_notifications_read(user_id):
    notifications = (
        Notification.active_query()
        .filter(Notification.user_id == user_id, Notification.is_read.is_(False))
        .all()
    )

    for notification in notifications:
        notification.is_read = True

    db.session.commit()
    return len(notifications)


def delete_notification(notification_id, user_id, is_admin=False):
    notification = _get_owned_notification(notification_id, user_id, is_admin=is_admin)
    notification.delete()
    return notification


def send_notification_to_user(target_user_id, title, message):
    user = User.get_by_id(target_user_id)
    if not user or user.is_deleted:
        raise NotificationServiceError("User not found", status_code=404)

    notification = Notification(
        user_id=user.id,
        title=title,
        message=message,
    )
    notification.save()
    return notification


def broadcast_notification(title, message):
    users = User.active_query().filter(User.is_active.is_(True)).all()

    notifications = []
    for user in users:
        notification = Notification(
            user_id=user.id,
            title=title,
            message=message,
        )
        db.session.add(notification)
        notifications.append(notification)

    db.session.commit()
    return len(notifications)
