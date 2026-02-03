from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.team_member import TeamMember

team_bp = Blueprint('team', __name__, url_prefix='/team')

@team_bp.route('/', methods=['GET'])
def index():
    members = TeamMember.query.all()
    return render_template('team/index.html', members=members)

@team_bp.route('/create', methods=['GET'])
def create():
    return render_template('team/create.html')

@team_bp.route('/store', methods=['POST'])
def store():
    name = request.form.get('name')
    role = request.form.get('role')
    email = request.form.get('email')
    
    # Basic validation
    if not name:
        flash("Name is required", "error")
        return redirect(url_for('team.create'))
        
    try:
        new_member = TeamMember(name=name, role=role, email=email)
        db.session.add(new_member)
        db.session.commit()
        flash("Team member added successfully", "success")
        return redirect(url_for('team.index'))
    except Exception as e:
        flash(f"Error adding member: {str(e)}", "error")
        return redirect(url_for('team.create'))

@team_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    member = TeamMember.query.get_or_404(id)
    return render_template('team/edit.html', member=member)

@team_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    member = TeamMember.query.get_or_404(id)
    member.name = request.form.get('name')
    member.role = request.form.get('role')
    member.email = request.form.get('email')
    
    try:
        db.session.commit()
        flash("Team member updated", "success")
        return redirect(url_for('team.index'))
    except Exception as e:
        flash(f"Error updating member: {str(e)}", "error")
        return redirect(url_for('team.edit', id=id))

@team_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    member = TeamMember.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash("Team member removed", "success")
    return redirect(url_for('team.index'))
