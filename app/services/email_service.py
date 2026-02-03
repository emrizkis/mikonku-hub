from flask_mail import Message
from flask import render_template, current_app
from app import mail
from threading import Thread

class EmailService:
    @staticmethod
    def send_async_email(app, msg):
        with app.app_context():
            mail.send(msg)

    @staticmethod
    def send_email(subject, recipient, template, **kwargs):
        app = current_app._get_current_object()
        msg = Message(subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
        msg.html = render_template(template, **kwargs)
        
        # Send asynchronously to avoid blocking the request/scheduler
        thr = Thread(target=EmailService.send_async_email, args=[app, msg])
        thr.start()

    @staticmethod
    def send_task_reminder(task, recipient_email, custom_message=None):
        EmailService.send_email(
            subject=f"Reminder: Task '{task.name}' is due in 3 days",
            recipient=recipient_email,
            template='emails/reminder.html',
            task=task,
            custom_message=custom_message
        )
