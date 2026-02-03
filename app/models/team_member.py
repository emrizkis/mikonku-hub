from app import db

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=True) # e.g. 'Developer', 'Designer'
    email = db.Column(db.String(120), unique=True, nullable=True)
    
    # Relationships
    tasks = db.relationship('Task', backref='assignee', lazy=True)

    def __repr__(self):
        return f'<TeamMember {self.name}>'
