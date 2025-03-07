from sqlalchemy import select
from sqlalchemy.orm import load_only
from server.extensions import db
from server.app.models import User

def get_all_users(user_id=None, role=None, email=None, is_active=None, username=None,):
    """Fetch users with optional filtering"""
    stmt = select(User).options(load_only(User.id, User.username, User.email, User.role, User.is_active))
    conditions = []
    if user_id:
        try:
            conditions.append(User.id == int(user_id))  # Ensure user_id is an integer
        except ValueError:
            return {"error": "Invalid user_id parameter"}, 400  # Return error if user_id is not a number
    if role:
        conditions.append(User.role == role)  # Exact match for role

    if username:
        conditions.append(User.username == username)  # Exact match for username

    if is_active is not None:  # ✅ Convert "true"/"false" string to Boolean
        if is_active.lower() == "true":
            conditions.append(User.is_active.is_(True))
        elif is_active.lower() == "false":
            conditions.append(User.is_active.is_(False))
        else:
            return {"error": "Invalid is_active parameter, expected 'true' or 'false'"}, 400

    if conditions:
        stmt = stmt.where(*conditions)

    result = db.session.execute(stmt)
    return result.scalars().all()  # ✅ Return all results as a list

def update_user_partially(user_id, data):
    """PATCH: Update specific user fields without modifying the entire record."""
    user = db.session.get(User, user_id)

    if not user:
        return {"error": "User not found"}, 404

    allowed_fields = {"username", "email", "first_name", "last_name", "role", "is_active"}  # ✅ Allowed updates

    for key, value in data.items():
        if key in allowed_fields:
            setattr(user, key, value.strip() if isinstance(value, str) else value)

    try:
        db.session.commit()
        return {"message": "User updated successfully", "user": user.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500

def delete_user(current_user_id, user_id):
    """Delete a user (Admins only)"""
    current_user = db.session.get(User, current_user_id)
    
    if not current_user or current_user.role != "admin":
        return {"error": "Access denied, only admins can delete users"}, 403

    user = db.session.get(User, user_id)
    
    if not user:
        return {"error": "User not found"}, 404

    db.session.delete(user)
    
    try:
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500
    
def soft_delete_user(current_user_id, user_id):
    """Soft delete a user (Admins only) by setting is_active=False."""
    current_user = db.session.get(User, current_user_id)

    if not current_user or current_user.role != "admin":
        return {"error": "Access denied, only admins can disable users"}, 403

    user = db.session.get(User, user_id)
    
    if not user:
        return {"error": "User not found"}, 404

    if not user.is_active:
        return {"error": "User is already disabled"}, 400

    user.is_active = False  # ✅ Soft delete by disabling the user

    try:
        db.session.commit()
        return {"message": "User disabled successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500
    
def enable_user(current_user_id, user_id):
    """Enable a previously disabled user (Admins only)."""
    current_user = db.session.get(User, current_user_id)

    if not current_user or current_user.role != "admin":
        return {"error": "Access denied, only admins can enable users"}, 403

    user = db.session.get(User, user_id)
    
    if not user:
        return {"error": "User not found"}, 404

    if user.is_active:
        return {"error": "User is already active"}, 400  # ✅ Prevent enabling active users

    user.is_active = True  # ✅ Reactivate the user

    try:
        db.session.commit()
        return {"message": "User enabled successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500


