from server.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Proposal(db.Model):
    __tablename__ = 'proposals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    site = db.Column(db.String(255), nullable=False)
    client = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected', 'in_review', name="proposal_status"), default='pending')
    budget = db.Column(db.Numeric(10, 2), nullable=True)
    deadline = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    attachments = db.Column(db.String(255), nullable=True)

    # Relationship to the User who created the proposal
    user = db.relationship('User', backref=db.backref('proposals', lazy=True))

    def __repr__(self):
        return f'<Proposal {self.name} - {self.status}>'

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


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.ForeignKey('proposals.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    proposal = db.relationship('Proposal', primaryjoin='Task.proposal_id == Proposal.id', backref='tasks')

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