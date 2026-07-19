import os
import logging
from logging.handlers import RotatingFileHandler

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Single shared instances used across the entire application.
# Initialized here (unbound) and attached to the app via init_extensions(app)
# to avoid circular imports between modules.

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
bcrypt = Bcrypt()
cors = CORS()


def init_extensions(app):
    """Bind all Flask extensions to the given app instance."""

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    _init_upload_folder(app)
    _init_logging(app)
    _init_jwt_callbacks()


def _init_jwt_callbacks():
    from app.utils.response import error_response
    from app.utils.token_blocklist import is_token_revoked

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_revoked(jwt_payload["jti"])

    @jwt.unauthorized_loader
    def custom_unauthorized_response(err_str):
        return error_response("Missing or invalid authorization token", status_code=401)

    @jwt.invalid_token_loader
    def custom_invalid_token_response(err_str):
        return error_response("Invalid token", status_code=422)

    @jwt.expired_token_loader
    def custom_expired_token_response(jwt_header, jwt_payload):
        return error_response("Token has expired", status_code=401)

    @jwt.revoked_token_loader
    def custom_revoked_token_response(jwt_header, jwt_payload):
        return error_response("Token has been revoked", status_code=401)

    @jwt.needs_fresh_token_loader
    def custom_needs_fresh_token_response(jwt_header, jwt_payload):
        return error_response("Fresh token required", status_code=401)


def _init_upload_folder(app):
    upload_folder = app.config.get("UPLOAD_FOLDER")
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)


def _init_logging(app):
    log_folder = app.config.get("LOG_FOLDER")
    if log_folder and not os.path.exists(log_folder):
        os.makedirs(log_folder, exist_ok=True)

    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"), logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    file_handler = RotatingFileHandler(
        os.path.join(log_folder, "schemehub.log"), maxBytes=1_000_000, backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    app.logger.addHandler(file_handler)

    # Most PaaS providers (Render included) only capture stdout/stderr and use
    # an ephemeral filesystem, so the file handler alone would lose all logs
    # on every restart/redeploy in production. A stdout handler keeps logs
    # visible in the platform's log dashboard regardless of deployment target.
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    app.logger.addHandler(stream_handler)

    app.logger.setLevel(log_level)
