from app import db

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # Relationship to Project is defined in Project model via backref, 
    # OR we can define it here. In original it was backref.
    # To avoid circular imports, let's keep it simple.
    # The backref in Project class handles the relationship.
    # Wait, Project class has: milestones = db.relationship('Milestone', backref='project', ...)
    # But wait, original code had `project = db.relationship('Project', backref=...)` in Milestone.
    # Let's clean this up. I put `milestones = ...` in Project model in project.py.
    # So here we just need the foreign key.
    
    def __repr__(self):
        return f'<Milestone {self.name}>'
