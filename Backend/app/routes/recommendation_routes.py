from flask import Blueprint

from app.controllers.recommendation_controller import (
    get_recommendations_controller,
    search_schemes_controller,
)

recommendation_bp = Blueprint("recommendations", __name__)
recommendation_bp.add_url_rule("", view_func=get_recommendations_controller, methods=["GET"])

search_bp = Blueprint("search", __name__)
search_bp.add_url_rule("", view_func=search_schemes_controller, methods=["GET"])
