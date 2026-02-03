from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from app import db
from app.models import Task, Project
from app.models.team_member import TeamMember

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Note: Tasks are usually related to a project.
# We might need to pass project_id to create/store.

@tasks_bp.route('/store/<int:project_id>', methods=['POST'])
def store(project_id):
    project = Project.query.get_or_404(project_id)
    name = request.form.get('name')
    
    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    plan_start_date = parse_date(request.form.get('plan_start_date'))
    plan_end_date = parse_date(request.form.get('plan_end_date'))
    actual_start_date = parse_date(request.form.get('actual_start_date'))
    actual_end_date = parse_date(request.form.get('actual_end_date'))
    
    status = request.form.get('status')
    progress = request.form.get('progress') or 0
    assigned_to_id = request.form.get('assigned_to_id')
    
    reminder_enabled = 'reminder_enabled' in request.form
    reminder_custom_message = request.form.get('reminder_custom_message')

    new_task = Task(
        name=name, 
        project_id=project.id, 
        plan_start_date=plan_start_date, 
        plan_end_date=plan_end_date,
        actual_start_date=actual_start_date,
        actual_end_date=actual_end_date,
        status=status, 
        progress=int(progress),
        assigned_to_id=assigned_to_id,
        reminder_enabled=reminder_enabled,
        reminder_custom_message=reminder_custom_message
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('projects.show', id=project.id))

@tasks_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    task = Task.query.get_or_404(id)
    members = TeamMember.query.all()
    return render_template('tasks/edit.html', task=task, members=members)

@tasks_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    task = Task.query.get_or_404(id)
    task.name = request.form.get('name')
    
    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    task.plan_start_date = parse_date(request.form.get('plan_start_date'))
    task.plan_end_date = parse_date(request.form.get('plan_end_date'))
    task.actual_start_date = parse_date(request.form.get('actual_start_date'))
    task.actual_end_date = parse_date(request.form.get('actual_end_date'))

    task.status = request.form.get('status')
    task.progress = int(request.form.get('progress') or 0)
    task.assigned_to_id = request.form.get('assigned_to_id')
    
    task.reminder_enabled = 'reminder_enabled' in request.form
    task.reminder_custom_message = request.form.get('reminder_custom_message')
    
    db.session.commit()
    return redirect(url_for('projects.show', id=task.project_id))

@tasks_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    task = Task.query.get_or_404(id)
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('projects.show', id=project_id))
