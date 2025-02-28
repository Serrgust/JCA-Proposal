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
    proposals = db.relationship('Proposal', backref='author', lazy=True)

    def set_password(self, password):
        """Hash the password before storing it"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the password against the stored hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} - {self.role}>'

