import sys
from datetime import datetime, timezone

import flask

APP_NAME = "SchemeHub"
APP_VERSION = "1.0.0"


def get_health_status():
    return {
        "status": "healthy",
        "application": APP_NAME,
        "version": APP_VERSION,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def get_system_info(debug_mode, environment, blueprint_count):
    return {
        "flask_version": flask.__version__,
        "python_version": sys.version.split()[0],
        "environment": environment,
        "debug_mode": debug_mode,
        "registered_blueprints_count": blueprint_count,
    }


def get_ping_response():
    return {"success": True, "message": "pong"}
