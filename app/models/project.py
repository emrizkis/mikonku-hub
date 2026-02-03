from app import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Planning Dates
    plan_start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    plan_end_date = db.Column(db.Date, nullable=True)
    
    # Actual Dates
    actual_start_date = db.Column(db.Date, nullable=True)
    actual_end_date = db.Column(db.Date, nullable=True)
    
    # Relationships
    tasks = db.relationship('Task', backref='project', lazy=True, cascade="all, delete-orphan")
    milestones = db.relationship('Milestone', backref='project', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Project {self.name}>'
