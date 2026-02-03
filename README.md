# Mikonku Hub - Project Management Tool

A Flask-based Project Management application designed to help teams organize projects, assign tasks, and track progress. Features include team management, Gantt charts, AI-assisted project generation, and automated email reminders.

## Features

- **Project Management**: Create and track projects.
- **Task Management**: Assign tasks to team members, set dates, and track status.
- **Team Management**: Manage team members and roles.
- **Gantt Chart**: Visual timeline of project tasks.
- **AI Projects**: Generate project structures using Gemini AI.
- **Email Reminders**: Automated email notifications for tasks due in 3 days.

## Prerequisites

- Python 3.8+
- SMTP Server (e.g., Gmail) for email features.

## Installation & Setup

### 1. Set up Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
# Create virtual environment named .venv
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory (based on the template below) to configure the application and email settings.

```bash
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=dev-key-very-secret
# DATABASE_URL=sqlite:///project_management.db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 4. Database Setup

Initialize the database using migrations.

```bash
# Apply migrations relative to database/migrations/ folder
flask db upgrade
```

## Running the Application

Start the development server:

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`.

## Background Jobs (Email Reminders)

This application uses **Flask-APScheduler** to run background jobs.

- **Check Reminders**: Runs automatically every day at **09:00 AM**.
  - Checks for tasks due in exactly 3 days.
  - Sends an email to the assignee if they have an email address and reminders are enabled for that task.

### Running Jobs Manually

To trigger the reminder check manually (e.g., for testing purposes):

1. Open the Flask shell:
   ```bash
   flask shell
   ```

2. Run dimensions manually:
   ```python
   from app.services.reminder_service import ReminderService
   ReminderService.check_upcoming_deadlines()
   ```

## Project Structure

- `app/`: Application source code.
  - `controllers/`: Request handlers (Blueprints).
  - `models/`: Database models.
  - `templates/`: HTML templates.
  - `services/`: Business logic (Email, Reminders, AI).
- `database/`: Database related files (migrations, seeders).
- `config.py`: Application configuration.
- `run.py`: Entry point.
# mikonku-hub
