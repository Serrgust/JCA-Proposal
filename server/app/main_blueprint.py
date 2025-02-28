import json
from flask import jsonify
from flask import Blueprint

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/home')
def home():
    return "Home Page"

@main_blueprint.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(
        {
            "users": ['Reynaldo',   # List of users
                      'Jorge', 
                      'Edgar', 
                      'Alessandra']
        }
    )
