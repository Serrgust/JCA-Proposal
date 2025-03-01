from flask import Blueprint, jsonify, request
from server.extensions import db
from sqlalchemy import select
from server.app.models import User, Proposal
from sqlalchemy.orm import load_only
from server.app.services import get_all_users, get_filtered_proposals, get_tasks_by_proposal, get_task_by_id

get_routes_blueprint = Blueprint("get_routes_blueprint", __name__)

@get_routes_blueprint.route("/users", methods=["GET"])
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
@get_routes_blueprint.route("/proposals", methods=["GET"])
def get_proposals():
    status = request.args.get("status")
    client = request.args.get("client")
    created_by = request.args.get("created_by")

    proposals = get_filtered_proposals(status, client, created_by)

    # If there's an error (e.g., invalid `created_by`), return it
    if isinstance(proposals, tuple) and "error" in proposals[0]:
        return jsonify(proposals[0]), proposals[1]

    return jsonify([p.to_dict() for p in proposals])

@get_routes_blueprint.route("/proposals/<proposal_id>/tasks", methods=["GET"])
def get_tasks_by_proposal_id(proposal_id):
    """Fetch all tasks for a proposal, with optional subtasks"""
    include_subtasks = request.args.get("include_subtasks", default="false").lower() == "true"

    tasks = get_tasks_by_proposal(proposal_id, include_subtasks=include_subtasks)

    # If there's an error (e.g., invalid proposal_id), return it
    if isinstance(tasks, tuple) and "error" in tasks[0]:
        return jsonify(tasks[0]), tasks[1]

    return jsonify(tasks)

@get_routes_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    """Fetch a specific task by ID, with optional proposal and subtasks"""
    include_proposal = request.args.get("include_proposal", default="false").lower() == "true"
    include_subtasks = request.args.get("include_subtasks", default="false").lower() == "true"

    task = get_task_by_id(task_id, include_proposal=include_proposal, include_subtasks=include_subtasks)

    # If there's an error (e.g., invalid task_id), return it
    if isinstance(task, tuple) and "error" in task[0]:
        return jsonify(task[0]), task[1]

    return jsonify(task)