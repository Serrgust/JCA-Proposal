from sqlalchemy import select
from sqlalchemy.orm import load_only
from server.extensions import db
from server.app.models import Task

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
