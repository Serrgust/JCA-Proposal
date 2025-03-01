from sqlalchemy import select
from sqlalchemy.orm import load_only
from server.extensions import db
from server.app.models import Task, User, Proposal

def get_all_users(user_id=None, role=None):
    """Fetch users with optional filtering by id and role"""
    stmt = select(User).options(load_only(User.id, User.username, User.email, User.first_name, User.last_name, User.role))

    # Apply filters dynamically
    conditions = []
    if user_id:
        try:
            conditions.append(User.id == int(user_id))  # Ensure user_id is an integer
        except ValueError:
            return {"error": "Invalid user_id parameter"}, 400  # Return error if user_id is not a number
    if role:
        conditions.append(User.role == role)  # Exact match for role

    if conditions:
        stmt = stmt.where(*conditions)  # Apply filters

    result = db.session.execute(stmt)
    return result.scalars().all()

def get_filtered_proposals(status=None, client=None, created_by=None):
    """Fetch proposals with filtering"""
    stmt = select(Proposal).options(
        load_only(
            Proposal.id, Proposal.name, Proposal.site, Proposal.client, 
            Proposal.status, Proposal.budget, Proposal.deadline, 
            Proposal.description, Proposal.created_at, Proposal.created_by
        )
    )

    conditions = []
    if status:
        conditions.append(Proposal.status == status)
    if client:
        conditions.append(Proposal.client.ilike(f"%{client}%"))  # Case-insensitive search
    if created_by:
        try:
            conditions.append(Proposal.created_by == int(created_by))
        except ValueError:
            return {"error": "Invalid created_by parameter"}, 400

    if conditions:
        stmt = stmt.where(*conditions)

    result = db.session.execute(stmt)
    return result.scalars().all()

def get_tasks_by_proposal(proposal_id, include_subtasks=False):
    """Fetch all tasks for a specific proposal, optionally including subtasks"""
    if not proposal_id.isdigit():  # Ensure proposal_id is numeric
        return {"error": "Invalid proposal_id parameter"}, 400

    stmt = select(Task).where(Task.proposal_id == int(proposal_id))
    result = db.session.execute(stmt)
    tasks = result.scalars().all()

    return [t.to_dict(include_subtasks=include_subtasks) for t in tasks]

def get_task_by_id(task_id, include_proposal=False, include_subtasks=False):
    """Fetch a single task by ID with optional proposal and subtasks"""
    if not task_id.isdigit():  # Ensure task_id is numeric
        return {"error": "Invalid task_id parameter"}, 400

    stmt = select(Task).where(Task.id == int(task_id))
    result = db.session.execute(stmt)
    task = result.scalars().first()

    if not task:
        return {"error": "Task not found"}, 404

    return task.to_dict(include_proposal=include_proposal, include_subtasks=include_subtasks)
