from flask import Flask
from werkzeug.exceptions import HTTPException
from app.utils.responses import error_response


def register_error_handlers(app: Flask):
    @app.errorhandler(400)
    def bad_request(e):
        return error_response("Bad request.", 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return error_response("Unauthorized. Please log in.", 401)

    @app.errorhandler(403)
    def forbidden(e):
        return error_response("You do not have permission to perform this action.", 403)

    @app.errorhandler(404)
    def not_found(e):
        return error_response("The requested resource was not found.", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error_response("This method is not allowed for this endpoint.", 405)

    @app.errorhandler(413)
    def payload_too_large(e):
        return error_response("The uploaded file is too large.", 413)

    @app.errorhandler(422)
    def unprocessable_entity(e):
        return error_response("Validation failed.", 422)

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.exception("Internal server error: %s", e)
        return error_response("An unexpected internal server error occurred.", 500)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return error_response(e.description or "An error occurred.", e.code)

    @app.errorhandler(Exception)
    def handle_uncaught_exception(e):
        app.logger.exception("Unhandled exception: %s", e)
        return error_response("An unexpected error occurred.", 500)
