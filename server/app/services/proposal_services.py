from sqlalchemy import select
from sqlalchemy.orm import load_only
from server.extensions import db
from server.app.models import Proposal

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