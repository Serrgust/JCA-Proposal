from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.orm import load_only
from server.extensions import db
from server.app.models import Proposal, Subtask, Task

def get_filtered_proposals(name=None, client=None, client_name=None, created_by=None):
    """Fetch proposals with filtering based on the latest Proposal model."""
    
    stmt = select(Proposal).options(
        load_only(
            Proposal.id, Proposal.name, Proposal.site, Proposal.client, Proposal.client_name, 
            Proposal.quote_number, Proposal.opportunity_status, Proposal.budget, 
            Proposal.description, Proposal.created_at, Proposal.created_by,
            Proposal.business_unit, Proposal.resource_name
        )
    )

    conditions = []
    
    if name and name.strip():
        conditions.append(Proposal.name.ilike(f"%{name.strip()}%"))  # Case-insensitive search
    if client and client.strip():
        conditions.append(Proposal.client.ilike(f"%{client.strip()}%"))  # Case-insensitive client search
    if client_name and client_name.strip():
        conditions.append(Proposal.client_name.ilike(f"%{client_name.strip()}%"))  # Case-insensitive client_name search
    if created_by:
        try:
            conditions.append(Proposal.created_by == int(created_by))
        except ValueError:
            return {"error": "Invalid created_by parameter"}, 400

    if conditions:
        stmt = stmt.where(*conditions)

    result = db.session.execute(stmt)
    return result.scalars().all()

def update_proposal(proposal_id, data):
    """Update an existing proposal with validation checks."""
    proposal = db.session.get(Proposal, proposal_id)
    
    if not proposal:
        return {"error": "Proposal not found"}, 404

    # Fields that can be updated
    allowed_fields = {
        "name", "site", "client", "quote_number", "client_name",
        "budget", "description", "created_by", "business_unit",
        "opportunity_status", "resource_name"
    }

    # Validation checks
    if not any(key in allowed_fields for key in data.keys()):
        return {"error": "No valid fields provided for update"}, 400

    if "name" in data and not data["name"].strip():
        return {"error": "Proposal name cannot be empty"}, 400

    if "budget" in data:
        try:
            data["budget"] = float(data["budget"])
            if data["budget"] < 0:
                return {"error": "Budget must be a positive number"}, 400
        except ValueError:
            return {"error": "Invalid budget format"}, 400

    if "opportunity_status" in data and data["opportunity_status"] not in {"Quote", "Approved", "Rejected", "Pending"}:
        return {"error": "Invalid opportunity status. Allowed: Quote, Approved, Rejected, Pending"}, 400

    if "created_by" in data:
        from server.app.models import User
        user = db.session.get(User, data["created_by"])
        if not user:
            return {"error": "User does not exist"}, 400

    for key, value in data.items():
        if key in allowed_fields and isinstance(value, str):
            setattr(proposal, key, value.strip())  # Clean up input

    try:
        db.session.commit()
        return {"message": "Proposal updated successfully", "proposal": proposal.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500

@jwt_required()
def create_proposal(data):
    """Creates a new proposal along with optional tasks and subtasks, requiring authentication"""
    
    required_fields = ["name", "site", "client", "quote_number", "client_name"]
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing required field: {field}"}, 400
    
    try:
        # Get the authenticated user ID
        user_id = get_jwt_identity()
        if not user_id:
            return {"error": "User authentication required"}, 401
        
        # Create Proposal
        proposal = Proposal(
            name=data["name"],
            site=data["site"],
            client=data["client"],
            quote_number=data["quote_number"],
            client_name=data["client_name"],
            budget=data.get("budget"),
            description=data.get("description"),
            business_unit=data.get("business_unit", "In House Project"),
            opportunity_status=data.get("opportunity_status", "Quote"),
            resource_name=data.get("resource_name", "Automation Team"),
            created_by=user_id  # Automatically set from JWT token
        )
        db.session.add(proposal)
        db.session.flush()  # Flush to get the proposal ID
        
        # Create Tasks (if provided)
        tasks = []
        for task_data in data.get("tasks", []):
            task = Task(
                proposal_id=proposal.id,
                title=task_data["title"],
                description=task_data.get("description"),
                order=task_data.get("order", 0)
            )
            db.session.add(task)
            db.session.flush()  # Flush to get the task ID
            
            # Create Subtasks (if provided)
            for subtask_data in task_data.get("subtasks", []):
                subtask = Subtask(
                    task_id=task.id,
                    title=subtask_data["title"],
                    hours=subtask_data.get("hours", 0),
                    order=subtask_data.get("order", 0)
                )
                db.session.add(subtask)
            
            tasks.append(task)
        
        db.session.commit()
        
        return {
            "message": "Proposal created successfully",
            "proposal": proposal.to_dict(),
            "tasks": [task.to_dict(include_subtasks=True) for task in tasks]
        }, 201
    
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
