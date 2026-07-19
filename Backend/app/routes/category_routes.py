from flask import Blueprint

from app.controllers.scheme_controller import list_categories_controller

category_bp = Blueprint("categories", __name__)

category_bp.add_url_rule("", view_func=list_categories_controller, methods=["GET"])
