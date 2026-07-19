from app.models.audit_log import AuditLog

DEFAULT_PER_PAGE = 20
MAX_PER_PAGE = 100
DEFAULT_LATEST_LIMIT = 10


class AuditServiceError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


def _paginate(query, args):
    page = max(int(args.get("page", 1) or 1), 1)
    per_page = min(max(int(args.get("per_page", DEFAULT_PER_PAGE) or DEFAULT_PER_PAGE), 1), MAX_PER_PAGE)

    pagination = query.order_by(AuditLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return {
        "items": [log.to_dict() for log in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
    }


def get_all_logs(args):
    return _paginate(AuditLog.active_query(), args)


def get_log_by_id(log_id):
    log = AuditLog.get_by_id(log_id)
    if not log or log.is_deleted:
        raise AuditServiceError("Audit log not found", status_code=404)
    return log


def get_logs_by_user(user_id, args):
    query = AuditLog.active_query().filter(AuditLog.user_id == user_id)
    return _paginate(query, args)


def get_logs_by_action(action, args):
    query = AuditLog.active_query().filter(AuditLog.action == action)
    return _paginate(query, args)


def get_latest_logs(limit=DEFAULT_LATEST_LIMIT):
    logs = (
        AuditLog.active_query()
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return [log.to_dict() for log in logs]
