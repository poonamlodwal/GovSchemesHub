from flask import Blueprint

from app.controllers.system_controller import (
    health_controller,
    info_controller,
    ping_controller,
)

system_bp = Blueprint("system", __name__)

system_bp.add_url_rule("/health", view_func=health_controller, methods=["GET"])
system_bp.add_url_rule("/info", view_func=info_controller, methods=["GET"])
system_bp.add_url_rule("/ping", view_func=ping_controller, methods=["GET"])
