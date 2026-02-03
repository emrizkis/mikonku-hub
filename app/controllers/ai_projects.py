
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from app import db
from app.models import Project, Task
from app.services.ai_service import AIService

ai_projects_bp = Blueprint('ai_projects', __name__, url_prefix='/projects/magic')

@ai_projects_bp.route('/', methods=['GET'])
def create():
    return render_template('projects/magic_create.html')

@ai_projects_bp.route('/', methods=['POST'])
def store():
    prompt = request.form.get('prompt')
    
    if not prompt:
        flash("Please provide a description for your project.", "error")
        return redirect(url_for('ai_projects.create'))

    # Call AI Service
    project_data = AIService.generate_project_plan(prompt)
    
    if "error" in project_data:
        flash(f"Error generating project: {project_data['error']}", "error")
        return redirect(url_for('ai_projects.create'))

    try:
        # Create Project
        plan_start_date = datetime.strptime(project_data.get('plan_start_date'), '%Y-%m-%d').date()
        plan_end_date = datetime.strptime(project_data.get('plan_end_date'), '%Y-%m-%d').date()
        
        new_project = Project(
            name=project_data.get('name'),
            description=project_data.get('description'),
            plan_start_date=plan_start_date,
            plan_end_date=plan_end_date,
            actual_start_date=None,
            actual_end_date=None
        )
        
        db.session.add(new_project)
        db.session.flush() # Flush to get the ID
        
        # Create Tasks
        for task_data in project_data.get('tasks', []):
            start_offset = task_data.get('start_offset_days', 0)
            duration = task_data.get('duration_days', 1)
            
            task_start_date = plan_start_date + timedelta(days=start_offset)
            task_end_date = task_start_date + timedelta(days=duration)
            
            new_task = Task(
                name=task_data.get('name'),
                project_id=new_project.id,
                plan_start_date=task_start_date,
                plan_end_date=task_end_date,
                status='Pending',
                progress=0
            )
            db.session.add(new_task)
            
        db.session.commit()
        
        flash("Magic Application created successfully!", "success")
        return redirect(url_for('projects.show', id=new_project.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while saving the project: {str(e)}", "error")
        return redirect(url_for('ai_projects.create'))
