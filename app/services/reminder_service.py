from datetime import datetime, timedelta
from app.models.task import Task
from app.services.email_service import EmailService
from flask import current_app

class ReminderService:
    @staticmethod
    def check_upcoming_deadlines():
        """
        Check for tasks due in exactly 3 days and send reminders.
        """
        print("Checking upcoming deadlines...")
        try:
            today = datetime.now().date()
            target_date = today + timedelta(days=3)
            
            # Find tasks due on target_date that are not completed and have reminders enabled
            tasks_due = Task.query.filter(
                Task.plan_end_date == target_date,
                Task.status != 'Completed',
                Task.reminder_enabled == True
            ).all()
            
            print(f"Found {len(tasks_due)} tasks due on {target_date} with reminders enabled")
            
            for task in tasks_due:
                if task.assignee and task.assignee.email:
                    print(f"Sending reminder for task: {task.name} to {task.assignee.email}")
                    EmailService.send_task_reminder(task, task.assignee.email, task.reminder_custom_message)
                else:
                    print(f"Task {task.name} has no assignee email, skipping.")
                    
        except Exception as e:
            print(f"Error checking deadlines: {e}")
