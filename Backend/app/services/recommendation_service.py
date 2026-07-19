from app.extensions import db
from app.models.user import User
from app.models.scheme import Scheme
from app.services.eligibility_engine import (
    build_profile_from_user,
    build_profile_from_search_args,
    evaluate_scheme_eligibility,
    calculate_recommendation_score,
    scheme_matches_search_filters,
)

SEARCH_SORT_FIELDS = {"title", "last_date", "created_at"}


class RecommendationServiceError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


def get_recommendations(user_id, limit=20):
    user = User.get_by_id(user_id)
    if not user or user.is_deleted:
        raise RecommendationServiceError("User not found", status_code=404)

    profile = build_profile_from_user(user)
    schemes = Scheme.active_query().all()

    results = []
    for scheme in schemes:
        is_eligible, unmet_reasons, reason_text = evaluate_scheme_eligibility(scheme, profile)
        score = calculate_recommendation_score(scheme, profile)

        results.append(
            {
                "scheme": scheme.to_dict(),
                "eligibility_status": "Eligible" if is_eligible else "Not Eligible",
                "recommendation_score": score,
                "reason": reason_text,
            }
        )

    results.sort(key=lambda r: r["recommendation_score"], reverse=True)

    return results[:limit]


def search_schemes(args):
    query = Scheme.active_query()

    keyword = (args.get("keyword") or args.get("search") or "").strip()
    if keyword:
        like = f"%{keyword}%"
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
    if sort_by not in SEARCH_SORT_FIELDS:
        sort_by = "created_at"
    sort_order = (args.get("sort_order") or "desc").lower()
    sort_column = getattr(Scheme, sort_by)
    query = query.order_by(sort_column.asc() if sort_order == "asc" else sort_column.desc())

    candidates = query.all()

    # Determine which eligibility rule types the searcher actually constrained.
    active_rule_types = set()
    if args.get("age") not in (None, ""):
        active_rule_types.update({"min_age", "max_age"})
    if args.get("income") not in (None, ""):
        active_rule_types.update({"min_income", "max_income"})
    if args.get("gender") not in (None, ""):
        active_rule_types.add("gender")
    if args.get("disability") is not None:
        active_rule_types.add("disability")
    if args.get("student") is not None:
        active_rule_types.add("student")

    profile = build_profile_from_search_args(args)

    filtered = [
        scheme
        for scheme in candidates
        if scheme_matches_search_filters(scheme, profile, active_rule_types)
    ]

    page = max(int(args.get("page", 1) or 1), 1)
    per_page = min(max(int(args.get("per_page", 10) or 10), 1), 100)

    total = len(filtered)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = filtered[start:end]

    return {
        "items": [scheme.to_dict() for scheme in page_items],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page if per_page else 0,
        "has_next": end < total,
        "has_prev": start > 0,
    }
