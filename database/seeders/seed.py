import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import create_app, db
from app.models import Project, Task
from datetime import datetime, timedelta

app = create_app()

def seed():
    with app.app_context():
        print("Clearing database...")
        db.drop_all()
        db.create_all()

        print("Seeding Projects...")
        
        # Project 1: Website Redesign
        p1 = Project(
            name="Website Redesign",
            description="Revamping the corporate website with a modern look and better UX.",
            plan_start_date=datetime(2026, 2, 1).date(),
            plan_end_date=datetime(2026, 3, 15).date(),
            actual_start_date=datetime(2026, 2, 2).date()
        )
        db.session.add(p1)
        db.session.commit() # Commit to get ID
        
        # Tasks for P1
        tasks_p1 = [
            Task(name="Requirements Gathering", project_id=p1.id, 
                 plan_start_date=datetime(2026, 2, 1).date(), plan_end_date=datetime(2026, 2, 5).date(),
                 actual_start_date=datetime(2026, 2, 2).date(), actual_end_date=datetime(2026, 2, 6).date(),
                 status="Completed", progress=100),
            Task(name="Design Mockups", project_id=p1.id, 
                 plan_start_date=datetime(2026, 2, 6).date(), plan_end_date=datetime(2026, 2, 15).date(),
                 actual_start_date=datetime(2026, 2, 7).date(),
                 status="In Progress", progress=40),
            Task(name="Frontend Development", project_id=p1.id, 
                 plan_start_date=datetime(2026, 2, 16).date(), plan_end_date=datetime(2026, 3, 5).date(),
                 status="Pending", progress=0),
            Task(name="Backend Integration", project_id=p1.id, 
                 plan_start_date=datetime(2026, 2, 20).date(), plan_end_date=datetime(2026, 3, 10).date(),
                 status="Pending", progress=0),
        ]
        db.session.add_all(tasks_p1)

        # Project 2: Mobile App Launch
        p2 = Project(
            name="Mobile App Launch",
            description="Launching the new iOS and Android application.",
            plan_start_date=datetime(2026, 2, 10).date(),
            plan_end_date=datetime(2026, 4, 1).date()
        )
        db.session.add(p2)
        db.session.commit()

        # Tasks for P2
        tasks_p2 = [
            Task(name="Market Research", project_id=p2.id, 
                 plan_start_date=datetime(2026, 2, 10).date(), plan_end_date=datetime(2026, 2, 20).date(),
                 status="Pending", progress=0),
            Task(name="App Store Submission", project_id=p2.id, 
                 plan_start_date=datetime(2026, 3, 25).date(), plan_end_date=datetime(2026, 3, 30).date(),
                 status="Pending", progress=0),
        ]
        db.session.add_all(tasks_p2)

        # Project 3: Internal Migration
        p3 = Project(
            name="Internal Migration",
            description="Migrating legacy systems to cloud infrastructure.",
            plan_start_date=datetime(2026, 3, 1).date(),
            plan_end_date=datetime(2026, 5, 1).date()
        )
        db.session.add(p3)
        db.session.commit()
        
        # Tasks for P3
        tasks_p3 = [
            Task(name="Database Backup", project_id=p3.id,
                 plan_start_date=datetime(2026, 3, 1).date(), plan_end_date=datetime(2026, 3, 3).date(),
                 status="Pending", progress=0)
        ]
        db.session.add_all(tasks_p3)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
