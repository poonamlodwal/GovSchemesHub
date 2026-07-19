from flask import Blueprint

from app.controllers.scheme_controller import (
    create_scheme_controller,
    list_schemes_controller,
    get_scheme_controller,
    update_scheme_controller,
    delete_scheme_controller,
    schemes_by_category_controller,
    schemes_by_state_controller,
)

scheme_bp = Blueprint("schemes", __name__)

scheme_bp.add_url_rule("", view_func=list_schemes_controller, methods=["GET"])
scheme_bp.add_url_rule("", view_func=create_scheme_controller, methods=["POST"], endpoint="create_scheme_controller")
scheme_bp.add_url_rule(
    "/category/<int:category_id>",
    view_func=schemes_by_category_controller,
    methods=["GET"],
)
scheme_bp.add_url_rule(
    "/state/<string:state>",
    view_func=schemes_by_state_controller,
    methods=["GET"],
)
scheme_bp.add_url_rule("/<int:scheme_id>", view_func=get_scheme_controller, methods=["GET"])
scheme_bp.add_url_rule(
    "/<int:scheme_id>",
    view_func=update_scheme_controller,
    methods=["PUT"],
    endpoint="update_scheme_controller",
)
scheme_bp.add_url_rule(
    "/<int:scheme_id>",
    view_func=delete_scheme_controller,
    methods=["DELETE"],
    endpoint="delete_scheme_controller",
)
