from sqlalchemy import select
from sqlalchemy.orm import load_only
from server.extensions import db
from server.app.models import Proposal

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