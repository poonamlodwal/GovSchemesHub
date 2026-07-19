from flask import Blueprint

from app.routes.auth_routes import auth_bp
from app.routes.scheme_routes import scheme_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(scheme_bp, url_prefix="/api/schemes")
