from flask import Blueprint, render_template, request
from app.models import Project
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

gantt_bp = Blueprint('gantt', __name__, url_prefix='/gantt')

@gantt_bp.route('/', methods=['GET'])
def index():
    all_projects = Project.query.all()
    
    # Filter projects based on request args
    selected_ids = request.args.getlist('p')
    if selected_ids:
        # Convert strings to integers safety
        selected_ids = [int(pid) for pid in selected_ids if pid.isdigit()]
        projects = [p for p in all_projects if p.id in selected_ids]
    else:
        # Default show all if no filter provided (or first load)
        # Note: If user unchecks ALL, list is empty -> show nothing? 
        # Or distinguish "no param" vs "empty param"? 
        # Typically "no param" = all. 
        # If user explicitly unchecks all, we might end up with empty list.
        # Let's assume if 'p' is present but empty, it's empty.
        # But initially 'p' is not present.
        if 'p' in request.args:
             projects = []
        else:
             projects = all_projects
             selected_ids = [p.id for p in all_projects]

    data = []
    
    for project in projects:
        for task in project.tasks:
            data.append(dict(
                Task=task.name,
                Start=task.plan_start_date.isoformat(),
                Finish=task.plan_end_date.isoformat(),
                Project=project.name,
                Status=task.status,
                Description=f"{project.name}: {task.name} ({task.progress}%)"
            ))
            
    if not data:
         graph_html = "No tasks to display."
    else:
        df = pd.DataFrame(data)
        
        # Sort by Project then Start date
        df.sort_values(by=['Project', 'Start'], ascending=[True, True], inplace=True)
        
        # Facet by Project to create the "Outer Label" effect (Grouping)
        fig = px.timeline(
            df, 
            x_start="Start", 
            x_end="Finish", 
            y="Task", 
            color="Project",
            hover_name="Description",
            facet_row="Project", # Creates the grouping
            title="Project Schedule",
            height=200 + (len(df['Project'].unique()) * 150) # Dynamic height based on projects
        )
        
        fig.update_yaxes(matches=None, title=None) # Allow independent Y axes if needed, remove titles
        
        fig.update_yaxes(autorange="reversed") # Top down
        
        # Ensure project order in facets matches our sort
        fig.update_layout(
             xaxis_title=None
        )
        
        # Highlight Weekends
        # Convert to datetime for logic
        df['Start_DT'] = pd.to_datetime(df['Start'])
        df['Finish_DT'] = pd.to_datetime(df['Finish'])
        
        min_date = df['Start_DT'].min()
        max_date = df['Finish_DT'].max()
        
        # Iterate through dates to find weekends
        # We start from min_date and go up to max_date
        current_date = min_date
        while current_date <= max_date:
            # 5 is Saturday, 6 is Sunday
            if current_date.weekday() >= 5: 
                fig.add_vrect(
                    x0=current_date, 
                    x1=current_date + pd.Timedelta(days=1), 
                    fillcolor="rgba(128, 128, 128, 0.15)", 
                    layer="below", 
                    line_width=0,
                )
            current_date += pd.Timedelta(days=1)
        
        # By default facet labels (annotations) are on the right. 
        # We can try to move them or leave them as the "Group Label"
        # Custom Tick Generation for "Month W-Num" (e.g., Jan W1, Jan W2)
        # Facet labels cleanup
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        
        # View Mode Logic
        view_mode = request.args.get('view', 'daily')
        if view_mode == 'weekly':
            # Custom Tick Generation for "Month W-Num" (e.g., Jan W1, Jan W2)
            # Use min_date/max_date calculated above
            
            # Create a date range for ticks (Weekly freq, starting Mondays)
            # Pad the range slightly to ensure we cover the edges
            start_tick = min_date - pd.Timedelta(days=7)
            end_tick = max_date + pd.Timedelta(days=7)
            dates = pd.date_range(start=start_tick, end=end_tick, freq='W-MON')
            
            tick_vals = []
            tick_text = []
            
            for d in dates:
                # Calculate week number relative to month
                # (Day - 1) // 7 + 1 gives 1st week, 2nd week, etc. of the month
                week_num_of_month = (d.day - 1) // 7 + 1
                label = f"{d.strftime('%b')} W{week_num_of_month}"
                
                tick_vals.append(d)
                tick_text.append(label)
                
            fig.update_xaxes(
                tickvals=tick_vals,
                ticktext=tick_text,
                tickmode="array"
            )
            
    # Add "Ghost Traces" for hidden projects so they appear in Legend
    # They should be 'legendonly' (grayed out)
    # This allows the interaction logic to work (clicking them triggers filtering)
    hidden_projects = [p for p in all_projects if p.id not in selected_ids]
    for p in hidden_projects:
        fig.add_trace(go.Bar(
            x=[None], y=[None],
            name=p.name,
            legendgroup=p.name,
            showlegend=True,
            visible='legendonly',
            orientation='h' # Match timeline orientation
        ))
        
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('gantt/index.html', 
                           graph_html=graph_html, 
                           view_mode=request.args.get('view', 'daily'),
                           all_projects=all_projects,
                           selected_ids=selected_ids)
