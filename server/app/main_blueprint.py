""" from datetime import datetime
import json
import pandas as pd
from flask import request
from flask import jsonify
from flask import Blueprint
from flask import send_file
# from server.app.heymodels import Proposal, SubTask, Task, User
from server.extensions import db
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from server.app.models import Proposal, Task, Subtask, User

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/home')
def home():
    return "Home Page"

@main_blueprint.route('/proposals', methods=['POST'])
def create_proposal():
    data = request.json
    new_proposal = Proposal(
        name=data['name'],
        site=data['site'],
        client=data['client'],
        status=data.get('status', 'pending'),
        budget=data.get('budget', None),
        deadline=datetime.strptime(data['deadline'], '%Y-%m-%d') if 'deadline' in data else None,
        description=data.get('description', ''),
        created_by=data['created_by']
    )
    db.session.add(new_proposal)
    db.session.commit()
    return jsonify({'message': 'Proposal created!', 'proposal_id': new_proposal.id}), 201

@main_blueprint.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    proposal_id = data['proposal_id']

    # Get the highest order in the existing tasks
    stmt = select(func.max(Task.order)).where(Task.proposal_id == proposal_id)
    max_order = db.session.execute(stmt).scalar() or 0

    new_task = Task(
        proposal_id=proposal_id,
        title=data['title'],
        description=data.get('description', ''),
        order=max_order + 1  # Assign the next order number
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created!', 'task_id': new_task.id}), 201

@main_blueprint.route('/subtasks', methods=['POST'])
def create_subtask():
    data = request.json
    task_id = data['task_id']

    # Get the highest order in the existing subtasks
    stmt = select(func.max(Subtask.order)).where(Subtask.task_id == task_id)
    max_order = db.session.execute(stmt).scalar() or 0

    new_subtask = Subtask(
        task_id=task_id,
        title=data['title'],
        hours=data.get('hours', 0.0),
        order=max_order + 1  # Assign the next order number
    )

    db.session.add(new_subtask)
    db.session.commit()

    return jsonify({'message': 'SubTask created!', 'subtask_id': new_subtask.id}), 201


@main_blueprint.route('/export-proposals', methods=['GET'])
def export_proposals():
    stmt = (
        select(Proposal)
        .options(joinedload(Proposal.tasks).joinedload(Task.subtasks))
    )
    proposals = db.session.execute(stmt).scalars().all()  # Uses Flask-SQLAlchemy's session

    data = []
    for proposal in proposals:
        for task in proposal.tasks:
            for subtask in task.subtasks:
                data.append({
                    'Proposal Name': proposal.name,
                    'Site': proposal.site,
                    'Client': proposal.client,
                    'Task Title': task.title,
                    'Task Description': task.description,
                    'SubTask Title': subtask.title,
                    'SubTask Hours': float(subtask.hours)
                })

    df = pd.DataFrame(data)
    file_path = 'proposals_export.xlsx'
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)
 """