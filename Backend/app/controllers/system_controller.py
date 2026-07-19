import os

from flask import jsonify, current_app

from app.services.system_service import get_health_status, get_system_info, get_ping_response
from app.utils.response import success_response, error_response


def health_controller():
    try:
        health = get_health_status()
    except Exception:
        return error_response("Something went wrong fetching health status", status_code=500)

    return success_response("Health check successful", data=health)


def info_controller():
    try:
        debug_mode = bool(current_app.config.get("DEBUG", False))
        environment = os.environ.get("FLASK_ENV", "production")
        blueprint_count = len(current_app.blueprints)

        info = get_system_info(debug_mode, environment, blueprint_count)
    except Exception:
        return error_response("Something went wrong fetching system info", status_code=500)

    return success_response("System info fetched successfully", data=info)


def ping_controller():
    try:
        return jsonify(get_ping_response()), 200
    except Exception:
        return error_response("Something went wrong", status_code=500)
