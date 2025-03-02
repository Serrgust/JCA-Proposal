""" from flask import Blueprint, jsonify, request
from server.extensions import db
from sqlalchemy import select
from server.app.models import User, Proposal
from sqlalchemy.orm import load_only
from server.app.services import get_all_users, get_filtered_proposals, get_tasks_by_proposal, get_task_by_id

routes_blueprint = Blueprint("routes_blueprint", __name__)

@routes_blueprint.route("/users", methods=["GET"])
def get_users():
    # Read query parameters from request
    user_id = request.args.get("id")
    role = request.args.get("role")

    # Get filtered users
    users = get_all_users(user_id=user_id, role=role)

    # If there's an error (e.g., invalid `id`), return it
    if isinstance(users, tuple) and "error" in users[0]:
        return jsonify(users[0]), users[1]

    return jsonify([u.to_dict() for u in users])

# Fetch all proposals with filtering
@routes_blueprint.route("/proposals", methods=["GET"])
def get_proposals():
    status = request.args.get("status")
    client = request.args.get("client")
    created_by = request.args.get("created_by")

    proposals = get_filtered_proposals(status, client, created_by)

    # If there's an error (e.g., invalid `created_by`), return it
    if isinstance(proposals, tuple) and "error" in proposals[0]:
        return jsonify(proposals[0]), proposals[1]

    return jsonify([p.to_dict() for p in proposals])

@routes_blueprint.route("/proposals/<proposal_id>/tasks", methods=["GET"])
def get_tasks(proposal_id):
    """Fetch all tasks for a proposal, with optional subtasks"""
    include_subtasks = request.args.get("include_subtasks", default="false").lower() == "true"

    tasks = get_tasks_by_proposal(proposal_id, include_subtasks=include_subtasks)

    # If there's an error (e.g., invalid proposal_id), return it
    if isinstance(tasks, tuple) and "error" in tasks[0]:
        return jsonify(tasks[0]), tasks[1]

    return jsonify(tasks)

@routes_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    """Fetch a specific task by ID, with optional proposal and subtasks"""
    include_proposal = request.args.get("include_proposal", default="false").lower() == "true"
    include_subtasks = request.args.get("include_subtasks", default="false").lower() == "true"

    task = get_task_by_id(task_id, include_proposal=include_proposal, include_subtasks=include_subtasks)

    # If there's an error (e.g., invalid task_id), return it
    if isinstance(task, tuple) and "error" in task[0]:
        return jsonify(task[0]), task[1]

    return jsonify(task)


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
 """