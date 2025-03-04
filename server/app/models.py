from server.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Proposal(db.Model):
    __tablename__ = 'proposals'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    site = db.Column(db.String(255), nullable=False)
    client = db.Column(db.String(255), nullable=False)
    quote_number = db.Column(db.String(20), nullable=False)
    client_name = db.Column(db.String(255), nullable=False)
    budget = db.Column(db.Numeric(10, 2), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    business_unit = db.Column(db.String(50), default="In House Project", nullable=False)
    opportunity_status = db.Column(db.String(50), default="Quote", nullable=False)
    resource_name = db.Column(db.String(255), default="Automation Team", nullable=False)

    # Relationship to the User who created the proposal
    user = db.relationship('User', backref=db.backref('proposals', lazy=True))
    
    def __repr__(self):
        return f'<Proposal {self.name} - {self.quote_number}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "site": self.site,
            "client": self.client,
            "quote_number": self.quote_number,
            "client_name": self.client_name,
            "budget": float(self.budget) if self.budget else None,  # Convert Decimal to float
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "created_by": self.user.to_dict() if self.user else None,  # Include the user details
            "business_unit": self.business_unit,
            "opportunity_status": self.opportunity_status,
            "resource_name": self.resource_name
        }

class Subtask(db.Model):
    __tablename__ = 'subtasks'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.ForeignKey('tasks.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    hours = db.Column(db.Integer, nullable=False, default=0)  # Changed to Integer
    order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    task = db.relationship('Task', primaryjoin='Subtask.task_id == Task.id', backref='subtasks')

    def to_dict(self):
        """Convert Subtask object to dictionary"""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "title": self.title,
            "hours": self.hours,
            "order": self.order,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.ForeignKey('proposals.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with Proposal
    proposal = db.relationship('Proposal', primaryjoin='Task.proposal_id == Proposal.id', backref='tasks')

    def to_dict(self, include_proposal=False, include_subtasks=False):
        """Convert Task object to dictionary, with optional proposal and subtasks"""
        task_dict = {
            "id": self.id,
            "proposal_id": self.proposal_id,
            "title": self.title,
            "description": self.description,
            "order": self.order,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

        if include_proposal:
            task_dict["proposal"] = self.proposal.to_dict() if self.proposal else None  # Include proposal details

        if include_subtasks:
            task_dict["subtasks"] = [s.to_dict() for s in self.subtasks]  # Include subtasks

        return task_dict

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    role = db.Column(db.Enum('user', 'admin', 'moderator', name="user_roles"), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # Fixed from Integer to Boolean
    last_login = db.Column(db.DateTime, nullable=True)

    # Password hashing methods
    def set_password(self, password):
        """Hash the password before storing it"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the password against the stored hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} - {self.role}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role
        }