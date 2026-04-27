from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    skills = db.Column(db.String(200), nullable=False) # Comma separated
    location = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Volunteer {self.name}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    issue_type = db.Column(db.String(50), nullable=False) # e.g. Health, Education, Food
    urgency_level = db.Column(db.Integer, nullable=False) # 1 (Low) to 5 (Critical)
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending') # Pending, In Progress, Completed
    
    # Priority score calculated by the smart prioritization system
    priority_score = db.Column(db.Integer, default=0)

    assigned_volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), nullable=True)
    assigned_volunteer = db.relationship('Volunteer', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f'<Task {self.title}>'
