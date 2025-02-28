import os
import sys
from flask import Blueprint, jsonify
from app import db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models import User
from app.models import Proposal

routes = Blueprint("routes", __name__)

@routes.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

def add_proposal():
    new_proposal = Proposal(
        name="New Project Proposal",
        site="New York",
        client="ABC Corporation",
        status="pending",
        budget=50000.00,
        deadline="2024-12-31",
        description="A new construction project for ABC Corporation.",
        created_by=1,  # Assuming user ID 1 exists
        attachments="uploads/proposal123.pdf"
    )
    db.session.add(new_proposal)
    db.session.commit()

    print(f"Proposal '{new_proposal.name}' added!")

def add_user():
    new_user = User(
        username="john_doe",
        email="john@example.com",
        first_name="John",
        last_name="Doe",
        role="user"
    )
    new_user.set_password("securepassword123")  # Hash and store password
    db.session.add(new_user)
    db.session.commit()

    print(f"User '{new_user.username}' added!")