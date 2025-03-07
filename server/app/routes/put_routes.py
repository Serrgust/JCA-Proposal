from flask import Blueprint, jsonify, request
from server.app.services.proposal_services import update_proposal
from server.extensions import db
from sqlalchemy import select
from server.app.models import User, Proposal
from sqlalchemy.orm import load_only

put_routes_blueprint = Blueprint("put_routes_blueprint", __name__)

@put_routes_blueprint.route('/proposals/<int:proposal_id>', methods=['PUT'])
def update_proposal_route(proposal_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    result, status_code = update_proposal(proposal_id, data)
    return jsonify(result), status_code