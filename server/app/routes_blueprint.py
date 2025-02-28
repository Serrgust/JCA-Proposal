from flask import Blueprint, jsonify, request
from server.extensions import db
from sqlalchemy import select
from server.app.heymodels import User, Proposal

routes_blueprint = Blueprint("routes_blueprint", __name__)

# Fetch all users
@routes_blueprint.route("/users", methods=["GET"])
def get_users():
    stmt = select(User)
    result = db.session.execute(stmt)  # Execute the statement
    users = result.scalars().all()  # Fetch all results as User objects

    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email, 
         "first_name":u.first_name, "last_name":u.last_name,"role": u.role} for u in users
    ])


# Add a proposal
@routes_blueprint.route("/add_proposal", methods=["POST"])
def add_proposal():
    data = request.json

    new_proposal = Proposal(
        name=data.get("name", "New Project Proposal"),
        site=data.get("site", "New York"),
        client=data.get("client", "ABC Corporation"),
        status=data.get("status", "pending"),
        budget=data.get("budget", 50000.00),
        deadline=data.get("deadline", "2024-12-31"),
        description=data.get("description", "A new construction project."),
        created_by=data.get("created_by", 1),  # Assuming user ID 1 exists
        attachments=data.get("attachments", "uploads/proposal123.pdf")
    )

    db.session.add(new_proposal)
    db.session.commit()

    return jsonify({"message": f"Proposal '{new_proposal.name}' added!", "proposal_id": new_proposal.id}), 201

# Add a new user
@routes_blueprint.route("/add_user", methods=["POST"])
def add_user():
    data = request.json

    new_user = User(
        username=data["username"],
        email=data["email"],
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        role=data.get("role", "user")
    )
    new_user.set_password(data["password"])  # Hash and store password

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User '{new_user.username}' added!", "user_id": new_user.id}), 201
