from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from app import db
from app.models import Project
from app.models.team_member import TeamMember

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/', methods=['GET'])
def index():
    projects = Project.query.all()
    return render_template('projects/index.html', projects=projects)

@projects_bp.route('/create', methods=['GET'])
def create():
    return render_template('projects/create.html')

@projects_bp.route('/store', methods=['POST'])
def store():
    name = request.form.get('name')
    description = request.form.get('description')
    
    # Helper to parse dates
    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        
    plan_start_date = parse_date(request.form.get('plan_start_date')) or datetime.utcnow().date()
    plan_end_date = parse_date(request.form.get('plan_end_date'))
    actual_start_date = parse_date(request.form.get('actual_start_date'))
    actual_end_date = parse_date(request.form.get('actual_end_date'))

    new_project = Project(
        name=name, 
        description=description, 
        plan_start_date=plan_start_date,
        plan_end_date=plan_end_date,
        actual_start_date=actual_start_date,
        actual_end_date=actual_end_date
    )
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('projects.index'))

@projects_bp.route('/<int:id>', methods=['GET'])
def show(id):
    project = Project.query.get_or_404(id)
    members = TeamMember.query.all()
    return render_template('projects/show.html', project=project, members=members)

@projects_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    project = Project.query.get_or_404(id)
    return render_template('projects/edit.html', project=project)

@projects_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    project = Project.query.get_or_404(id)
    project.name = request.form.get('name')
    project.description = request.form.get('description')
    
    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    plan_start = request.form.get('plan_start_date')
    if plan_start:
         project.plan_start_date = parse_date(plan_start)
         
    project.plan_end_date = parse_date(request.form.get('plan_end_date'))
    project.actual_start_date = parse_date(request.form.get('actual_start_date'))
    project.actual_end_date = parse_date(request.form.get('actual_end_date'))
    
    db.session.commit()
    return redirect(url_for('projects.show', id=id))

@projects_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects.index'))
