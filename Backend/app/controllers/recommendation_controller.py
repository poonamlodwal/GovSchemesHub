from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.recommendation_service import (
    RecommendationServiceError,
    get_recommendations,
    search_schemes,
)
from app.utils.response import success_response, error_response


@jwt_required()
def get_recommendations_controller():
    identity = get_jwt_identity()
    limit = request.args.get("limit", 20)

    try:
        limit = int(limit)
    except (TypeError, ValueError):
        return error_response("Validation failed", ["limit must be an integer"], status_code=422)

    try:
        recommendations = get_recommendations(int(identity), limit=limit)
    except RecommendationServiceError as e:
        return error_response(e.message, e.errors, status_code=e.status_code)
    except Exception:
        return error_response("Something went wrong generating recommendations", status_code=500)

    return success_response(
        "Recommendations fetched successfully",
        data={"recommendations": recommendations, "total": len(recommendations)},
    )


def search_schemes_controller():
    try:
        results = search_schemes(request.args)
    except Exception:
        return error_response("Something went wrong performing the search", status_code=500)

    return success_response("Search results fetched successfully", data=results)
