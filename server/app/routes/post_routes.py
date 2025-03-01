from flask import Blueprint, jsonify, request
from server.extensions import db
from sqlalchemy import select
from server.app.models import User, Proposal
from sqlalchemy.orm import load_only
from server.app.services import get_all_users, get_filtered_proposals, get_tasks_by_proposal, get_task_by_id

post_routes_blueprint = Blueprint("post_routes_blueprint", __name__)