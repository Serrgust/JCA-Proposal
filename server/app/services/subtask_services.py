from sqlalchemy import select
from server.extensions import db
from server.app.models import Subtask

def get_subtasks_by_task(task_id):
    """Fetch all subtasks for a specific task"""
    try:
        task_id = int(task_id)
    except ValueError:
        return {"error": "Invalid task_id parameter"}, 400

    stmt = select(Subtask).where(Subtask.task_id == task_id)
    result = db.session.execute(stmt)
    return [s.to_dict() for s in result.scalars().all()]
