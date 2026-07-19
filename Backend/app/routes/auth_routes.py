from flask import Blueprint

from app.controllers.auth_controller import (
    register_controller,
    login_controller,
    refresh_controller,
    me_controller,
    logout_controller,
)

auth_bp = Blueprint("auth", __name__)

auth_bp.add_url_rule("/register", view_func=register_controller, methods=["POST"])
auth_bp.add_url_rule("/login", view_func=login_controller, methods=["POST"])
auth_bp.add_url_rule("/refresh", view_func=refresh_controller, methods=["POST"])
auth_bp.add_url_rule("/me", view_func=me_controller, methods=["GET"])
auth_bp.add_url_rule("/logout", view_func=logout_controller, methods=["POST"])
