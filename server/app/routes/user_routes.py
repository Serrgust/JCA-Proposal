from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.app.services.user_services import get_all_users, update_user_partially, delete_user, soft_delete_user, enable_user

user_routes_blueprint = Blueprint("user_routes_blueprint", __name__)

@user_routes_blueprint.route("/all", methods=["GET"])
def get_users_route():
    """Fetch all users with optional filtering"""
    user_id = request.args.get("user_id")
    role = request.args.get("role")
    email = request.args.get("email")
    username = request.args.get("username")
    is_active = request.args.get("is_active")

    result = get_all_users(user_id, role, email, username, is_active)
    
    if isinstance(result, tuple):  # If an error tuple is returned
        return jsonify(result[0]), result[1]
    
    return jsonify([user.to_dict() for user in result]), 200

@user_routes_blueprint.route("/<int:user_id>", methods=["PATCH"])
@jwt_required()
def update_user_route(user_id):
    """PATCH: Update specific fields of a user."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    result, status_code = update_user_partially(user_id, data)
    return jsonify(result), status_code

@user_routes_blueprint.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_route(user_id):
    """Delete a user (Admins only)"""
    current_user_id = get_jwt_identity()
    
    result, status_code = delete_user(current_user_id, user_id)
    return jsonify(result), status_code

@user_routes_blueprint.route("/<int:user_id>/disable", methods=["DELETE"])
@jwt_required()
def disable_user_route(user_id):
    """Soft delete a user (set is_active = False)"""
    current_user_id = get_jwt_identity()

    result, status_code = soft_delete_user(current_user_id, user_id)
    return jsonify(result), status_code

@user_routes_blueprint.route("/<int:user_id>/enable", methods=["PATCH"])
@jwt_required()
def enable_user_route(user_id):
    """Enable a user (set is_active = True)"""
    current_user_id = get_jwt_identity()

    result, status_code = enable_user(current_user_id, user_id)
    return jsonify(result), status_code


