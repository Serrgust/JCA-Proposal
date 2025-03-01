from sqlalchemy import select
from sqlalchemy.orm import load_only
from server.extensions import db
from server.app.models import User

def get_all_users(user_id=None, role=None):
    """Fetch users with optional filtering by id and role"""
    stmt = select(User).options(load_only(User.id, User.username, User.email, User.first_name, User.last_name, User.role))

    conditions = []
    if user_id:
        try:
            conditions.append(User.id == int(user_id))  # Ensure user_id is an integer
        except ValueError:
            return {"error": "Invalid user_id parameter"}, 400  # Return error if user_id is not a number
    if role:
        conditions.append(User.role == role)  # Exact match for role

    if conditions:
        stmt = stmt.where(*conditions)  # ✅ Apply filters correctly

    result = db.session.execute(stmt)
    return result.scalars().all()  # ✅ Return all results as a list
