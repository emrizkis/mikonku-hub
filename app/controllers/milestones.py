from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from app import db
from app.models import Project
import pandas as pd
import plotly.express as px
import plotly.io as pio

milestones_bp = Blueprint('milestones', __name__, url_prefix='/milestones')

@milestones_bp.route('/', methods=['GET'])
def index():
    projects = Project.query.all()
    
    # Chart Data derived from Projects
    data = []
    
    for p in projects:
        # 1. Project Start Milestone
        data.append(dict(
            Milestone="Start (Plan)",
            Date=p.plan_start_date.isoformat(),
            Project=p.name,
            Description=f"{p.name} Start: {p.plan_start_date}"
        ))
        
        # 2. Project Finish Milestone (Based on latest task)
        if p.tasks:
            max_date = max(t.plan_end_date for t in p.tasks)
            data.append(dict(
                Milestone="Finish (Plan)",
                Date=max_date.isoformat(),
                Project=p.name,
                Description=f"{p.name} Finish: {max_date}"
            ))
        
    if not data:
        graph_html = "No project data available."
    else:
        df = pd.DataFrame(data)
        
        # Scatter plot for milestones
        fig = px.scatter(
            df, 
            x="Date", 
            y="Project", 
            color="Milestone", # Color by Start/Finish
            symbol="Milestone",
            text="Milestone",
            hover_name="Description",
            title="Project Key Dates",
            size_max=15
        )
        
        fig.update_traces(marker=dict(size=14))
        fig.update_traces(textposition='top center')
        
        fig.update_layout(
             xaxis_title="Date",
             yaxis_title=None,
             height=400 + (len(projects) * 30)
        )
        
        graph_html = pio.to_html(fig, full_html=False)

    return render_template('milestones/index.html', graph_html=graph_html)
