from flask import Flask, jsonify

from app.config import get_config
from app.extensions import init_extensions


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(get_config())

    init_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)

    return app


def _register_blueprints(app):
    """
    Register route blueprints as each module is implemented.
    Blueprints are imported lazily inside this function to avoid
    circular imports with the extensions/db objects.
    """
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.routes.scheme_routes import scheme_bp
    app.register_blueprint(scheme_bp, url_prefix="/api/schemes")

    from app.routes.category_routes import category_bp
    app.register_blueprint(category_bp, url_prefix="/api/categories")

    from app.routes.recommendation_routes import recommendation_bp, search_bp
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommendations")
    app.register_blueprint(search_bp, url_prefix="/api/search")

    from app.routes.document_routes import document_bp
    app.register_blueprint(document_bp, url_prefix="/api/documents")

    from app.routes.chat_routes import chat_bp
    app.register_blueprint(chat_bp, url_prefix="/api/chat")

    from app.routes.notification_routes import notification_bp, admin_notification_bp
    app.register_blueprint(notification_bp, url_prefix="/api/notifications")
    app.register_blueprint(admin_notification_bp, url_prefix="/api/admin/notifications")

    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix="/api/admin/dashboard")

    from app.routes.audit_routes import audit_bp
    app.register_blueprint(audit_bp, url_prefix="/api/admin/audit")

    from app.routes.system_routes import system_bp
    app.register_blueprint(system_bp, url_prefix="/api/system")


def _register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "message": "Resource not found", "errors": []}),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {"success": False, "message": "Method not allowed", "errors": []}
            ),
            405,
        )

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception("Internal server error")
        return (
            jsonify(
                {"success": False, "message": "Internal server error", "errors": []}
            ),
            500,
        )
