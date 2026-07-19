from datetime import datetime

from app.extensions import db
from app.models.scheme import Scheme
from app.models.category import Category

ALLOWED_SORT_FIELDS = {"title", "last_date", "created_at"}


class SchemeServiceError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


def _get_active_category(category_id):
    category = Category.get_by_id(int(category_id))
    if not category or category.is_deleted:
        raise SchemeServiceError("Category not found", status_code=404)
    return category


def create_scheme(data):
    category = _get_active_category(data.get("category_id"))

    last_date = None
    if data.get("last_date"):
        last_date = datetime.strptime(data["last_date"], "%Y-%m-%d").date()

    scheme = Scheme(
        title=data.get("title").strip(),
        description=data.get("description"),
        benefits=data.get("benefits"),
        eligibility_summary=data.get("eligibility_summary"),
        application_process=data.get("application_process"),
        official_link=data.get("official_link"),
        last_date=last_date,
        state=data.get("state"),
        category_id=category.id,
    )
    scheme.save()
    return scheme


def update_scheme(scheme_id, data):
    scheme = get_scheme_by_id(scheme_id)

    if "category_id" in data and data.get("category_id"):
        category = _get_active_category(data.get("category_id"))
        scheme.category_id = category.id

    simple_fields = (
        "title",
        "description",
        "benefits",
        "eligibility_summary",
        "application_process",
        "official_link",
        "state",
    )
    for field in simple_fields:
        if field in data and data[field] is not None:
            setattr(scheme, field, data[field])

    if "last_date" in data and data.get("last_date"):
        scheme.last_date = datetime.strptime(data["last_date"], "%Y-%m-%d").date()

    db.session.commit()
    return scheme


def delete_scheme(scheme_id):
    scheme = get_scheme_by_id(scheme_id)
    scheme.soft_delete()
    return scheme


def get_scheme_by_id(scheme_id):
    scheme = Scheme.get_by_id(scheme_id)
    if not scheme or scheme.is_deleted:
        raise SchemeServiceError("Scheme not found", status_code=404)
    return scheme


def list_schemes(args):
    query = Scheme.active_query()

    search = (args.get("search") or "").strip()
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Scheme.title.ilike(like),
                Scheme.description.ilike(like),
                Scheme.benefits.ilike(like),
            )
        )

    category_id = args.get("category_id")
    if category_id:
        query = query.filter(Scheme.category_id == int(category_id))

    state = args.get("state")
    if state:
        query = query.filter(Scheme.state.ilike(state))

    sort_by = args.get("sort_by", "created_at")
    if sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "created_at"
    sort_order = (args.get("sort_order") or "desc").lower()
    sort_column = getattr(Scheme, sort_by)
    query = query.order_by(
        sort_column.asc() if sort_order == "asc" else sort_column.desc()
    )

    page = max(int(args.get("page", 1) or 1), 1)
    per_page = min(max(int(args.get("per_page", 10) or 10), 1), 100)

    return query.paginate(page=page, per_page=per_page, error_out=False)


def list_schemes_by_category(category_id):
    _get_active_category(category_id)
    return Scheme.active_query().filter(Scheme.category_id == category_id).all()


def list_schemes_by_state(state):
    return Scheme.active_query().filter(Scheme.state.ilike(state)).all()


def list_categories():
    return Category.active_query().all()
