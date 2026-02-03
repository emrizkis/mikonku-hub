from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_apscheduler import APScheduler

db = SQLAlchemy()
mail = Mail()
scheduler = APScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        # models imported in controllers
        from . import models

    from app.controllers.projects import projects_bp
    from app.controllers.tasks import tasks_bp
    from app.controllers.gantt import gantt_bp
    from app.controllers.milestones import milestones_bp

    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(gantt_bp)
    app.register_blueprint(milestones_bp)
    
    from app.controllers.ai_projects import ai_projects_bp
    app.register_blueprint(ai_projects_bp)
    
    from app.controllers.team import team_bp
    app.register_blueprint(team_bp)
    
    from flask_migrate import Migrate
    migrate = Migrate(app, db, directory='database/migrations')
    
    # Register Scheduler Jobs
    from app.services.reminder_service import ReminderService
    
    # Check for reminders every day at 09:00 AM
    @scheduler.task('cron', id='check_reminders', hour=9)
    def check_reminders():
        with app.app_context():
            ReminderService.check_upcoming_deadlines()

    # Redirect root to projects index
    from flask import redirect, url_for
    @app.route('/')
    def index():
        return redirect(url_for('projects.index'))

    return app
