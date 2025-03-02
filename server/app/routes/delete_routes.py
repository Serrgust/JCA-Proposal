from flask import Blueprint, jsonify, request
from server.extensions import db
from sqlalchemy import select
from server.app.models import User, Proposal
from sqlalchemy.orm import load_only

delete_routes_blueprint = Blueprint("delete_routes_blueprint", __name__)