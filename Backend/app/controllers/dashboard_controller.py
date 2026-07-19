from app.services.dashboard_service import (
    get_dashboard_summary,
    get_statistics,
    get_recent_users,
    get_recent_documents,
    get_recent_notifications,
)
from app.utils.response import success_response, error_response
from app.utils.decorators import role_required


@role_required("admin")
def get_dashboard_summary_controller():
    try:
        summary = get_dashboard_summary()
    except Exception:
        return error_response("Something went wrong fetching the dashboard summary", status_code=500)

    return success_response("Dashboard summary fetched successfully", data=summary)


@role_required("admin")
def get_statistics_controller():
    try:
        statistics = get_statistics()
    except Exception:
        return error_response("Something went wrong fetching statistics", status_code=500)

    return success_response("Statistics fetched successfully", data=statistics)


@role_required("admin")
def get_recent_users_controller():
    try:
        users = get_recent_users()
    except Exception:
        return error_response("Something went wrong fetching recent users", status_code=500)

    return success_response("Recent users fetched successfully", data=users)


@role_required("admin")
def get_recent_documents_controller():
    try:
        documents = get_recent_documents()
    except Exception:
        return error_response("Something went wrong fetching recent documents", status_code=500)

    return success_response("Recent documents fetched successfully", data=documents)


@role_required("admin")
def get_recent_notifications_controller():
    try:
        notifications = get_recent_notifications()
    except Exception:
        return error_response(
            "Something went wrong fetching recent notifications", status_code=500
        )

    return success_response("Recent notifications fetched successfully", data=notifications)
