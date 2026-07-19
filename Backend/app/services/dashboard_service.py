from app.models.user import User
from app.models.scheme import Scheme
from app.models.uploaded_document import UploadedDocument
from app.models.notification import Notification
from app.models.recommendation import Recommendation
from app.models.chat_history import ChatHistory

RECENT_ITEMS_LIMIT = 10


def get_statistics():
    return {
        "total_users": User.active_query().count(),
        "total_schemes": Scheme.active_query().count(),
        "total_documents": UploadedDocument.active_query().count(),
        "total_notifications": Notification.active_query().count(),
        "total_recommendations": Recommendation.active_query().count(),
        "total_chat_records": ChatHistory.active_query().count(),
    }


def get_recent_users(limit=RECENT_ITEMS_LIMIT):
    users = User.active_query().order_by(User.created_at.desc()).limit(limit).all()
    return [user.to_dict() for user in users]


def get_recent_documents(limit=RECENT_ITEMS_LIMIT):
    documents = (
        UploadedDocument.active_query()
        .order_by(UploadedDocument.created_at.desc())
        .limit(limit)
        .all()
    )
    return [document.to_dict() for document in documents]


def get_recent_notifications(limit=RECENT_ITEMS_LIMIT):
    notifications = (
        Notification.active_query().order_by(Notification.created_at.desc()).limit(limit).all()
    )
    return [notification.to_dict() for notification in notifications]


def get_dashboard_summary():
    return {
        "statistics": get_statistics(),
        "recent_users": get_recent_users(),
        "recent_documents": get_recent_documents(),
        "recent_notifications": get_recent_notifications(),
    }
