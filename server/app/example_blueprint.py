from flask import Blueprint, jsonify

example_blueprint = Blueprint('example_blueprint', __name__)

@example_blueprint.route('/')
def index():
    return "This is an example app"

@example_blueprint.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(
        {
            "users": ['Reynaldo',   # List of users
                      'Jorge', 
                      'Edgar', 
                      'Alessandra']
        }
    )

@example_blueprint.route("/api/proposals", methods=["GET"])
def get_proposals():
    return jsonify(
        {
            "proposals": ['Project A',   # List of proposals
                          'Project B', 
                          'Project C', 
                          'Project D']
        }
    )

@example_blueprint.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(
        {
            "tasks": ['Task 1',   # List of tasks
                      'Task 2', 
                      'Task 3', 
                      'Task 4']
        }
    )

@example_blueprint.route("/api/subtasks", methods=["GET"])
def get_subtasks():
    return jsonify(
        {
            "subtasks": ['Subtask 1',   # List of subtasks
                         'Subtask 2', 
                         'Subtask 3', 
                         'Subtask 4']
        }
    )

@example_blueprint.route("/api/roles", methods=["GET"])
def get_roles():
    return jsonify(
        {
            "roles": ['User',   # List of roles
                      'Admin', 
                      'Moderator']
        }
    )