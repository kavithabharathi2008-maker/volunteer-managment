from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False) # NGO, Volunteer, Admin
    location = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(128), nullable=True) # Simple storage for demo

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # Food, Health, Education, etc.
    urgency = db.Column(db.Integer, nullable=False) # 1 (Low) to 5 (Critical)
    description = db.Column(db.Text, nullable=False)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    reported_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Issue {self.category} at {self.location}>'

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200), nullable=False) # Comma separated
    availability = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    user = db.relationship('User', backref=db.backref('volunteer_profile', uselist=False))

    def __repr__(self):
        return f'<Volunteer {self.name}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), nullable=True)
    status = db.Column(db.String(20), default='Pending') # Pending, In Progress, Completed
    priority_score = db.Column(db.Integer, default=0)
    
    issue = db.relationship('Issue', backref=db.backref('tasks', lazy=True))
    volunteer = db.relationship('Volunteer', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f'<Task Issue:{self.issue_id} Vol:{self.volunteer_id} Status:{self.status}>'
