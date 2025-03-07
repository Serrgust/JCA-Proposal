from flask import Blueprint, request, jsonify
from functools import wraps  # Import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import select
from server.extensions import db
from server.app.models import User

auth_routes_blueprint = Blueprint("auth_routes_blueprint", __name__)

# Role-based access control decorator
def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)  # Preserve function name
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            stmt = select(User).where(User.id == current_user_id)
            user = db.session.execute(stmt).scalar_one_or_none()

            if not user or user.role.lower() != required_role.lower():
                return jsonify({"error": "Access denied, insufficient permissions"}), 403
            
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper

@auth_routes_blueprint.route("/register", methods=["POST"])
def register():
    """Register a new user with hashed password"""
    data = request.get_json()
    
    required_fields = ["username", "first_name", "last_name", "email", "password", "role"]
    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    stmt = select(User).where(User.email == data["email"].strip())
    existing_user = db.session.execute(stmt).scalar_one_or_none()

    if existing_user:
        return jsonify({"error": "Email is already registered"}), 400
    
    hashed_password = generate_password_hash(data["password"].strip())
    user = User(
        username=data["username"].strip(),
        first_name=data["first_name"].strip(),
        last_name=data["last_name"].strip(),
        email=data["email"].strip(),
        role=data["role"].strip().lower(),
        password_hash=hashed_password
    )
    
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_routes_blueprint.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return a JWT"""
    data = request.get_json()
    
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400
    
    stmt = select(User).where(User.email == data["email"].strip())
    user = db.session.execute(stmt).scalar_one_or_none()

    if not user or not check_password_hash(user.password_hash, data["password"].strip()):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Login successful", "access_token": access_token}), 200

@auth_routes_blueprint.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Return the currently authenticated user's info"""
    current_user_id = get_jwt_identity()
    stmt = select(User).where(User.id == current_user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role
    }), 200

@auth_routes_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """Example of a protected route that requires authentication"""
    current_user_id = get_jwt_identity()
    return jsonify({"message": "Access granted", "user_id": current_user_id}), 200

@auth_routes_blueprint.route("/admin-only", methods=["GET"])
@role_required("admin")
def admin_only():
    """Example route restricted to admin users"""
    return jsonify({"message": "Access granted, admin permissions verified"}), 200

@auth_routes_blueprint.route("/moderator-only", methods=["GET"])
@role_required("moderator")
def moderator_only():
    """Example route restricted to moderator users"""
    return jsonify({"message": "Access granted, moderator permissions verified"}), 200
