from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('team_member.id'), nullable=True)
    
    # Planning Dates
    plan_start_date = db.Column(db.Date, nullable=False)
    plan_end_date = db.Column(db.Date, nullable=False)
    
    # Actual Dates
    actual_start_date = db.Column(db.Date, nullable=True)
    actual_end_date = db.Column(db.Date, nullable=True)
    
    status = db.Column(db.String(20), default='Pending') # Pending, In Progress, Completed
    progress = db.Column(db.Integer, default=0) # 0-100

    # Reminder
    reminder_enabled = db.Column(db.Boolean, default=False)
    reminder_custom_message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Task {self.name}>'
