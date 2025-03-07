from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from server.app.services.proposal_services import create_proposal

post_routes_blueprint = Blueprint("post_routes_blueprint", __name__)

@post_routes_blueprint.route("/proposals", methods=["POST"])
@jwt_required()
def create_proposal_route():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    result, status_code = create_proposal(data)
    return jsonify(result), status_code
