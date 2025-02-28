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
    budget = db.Column(db.Numeric(10,2), nullable=True)
    deadline = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attachments = db.Column(db.String(255), nullable=True)  # File path for attachments

    # Relationship to the User who created the proposal
    user = db.relationship('User', backref=db.backref('proposals', lazy=True))

    def __repr__(self):
        return f'<Proposal {self.name} - {self.status}>'
    
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
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationship: One user can have multiple proposals
    # proposals = db.relationship('Proposal', backref='author', lazy=True)
    # The backref='proposals' in Proposal already creates a user.proposals property, so there's no need to redefine it in User.

    def set_password(self, password):
        """Hash the password before storing it"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the password against the stored hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} - {self.role}>'

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'), nullable=False, index=True)  # Indexed foreign key
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=False, default=0)  # Order in the proposal
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with Proposal
    proposal = db.relationship('Proposal', backref=db.backref('tasks', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<Task {self.title} in Proposal {self.proposal_id}>'
    
class Subtask(db.Model):
    __tablename__ = 'subtasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    hours = db.Column(db.Numeric(5, 2), nullable=False, default=0.0)  # Default hours to 0
    order = db.Column(db.Integer, nullable=False, default=0)  # Default order to 0
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with Task (Ensures cascading delete at both ORM & DB level)
    task = db.relationship('Task', backref=db.backref('subtasks', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<Subtask {self.title} in Task {self.task_id}>'

