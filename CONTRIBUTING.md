# Developer Guide & Contribution Rules

This document outlines the coding standards and architectural patterns for **Mikonku Hub**. Please follow these rules to maintain code quality and consistency.

## 1. Architecture: Resourceful MVC
We use a Resourceful MVC pattern built on Flask Blueprints.

*   **Controllers**: Located in `app/controllers/`.
    *   Each feature gets its own controller (e.g., `projects.py`, `tasks.py`).
    *   Follow standard resourceful naming:
        *   `index()`: List resources (GET)
        *   `create()`: Show creation form (GET)
        *   `store()`: Save new resource (POST)
        *   `show(id)`: Show specific resource (GET)
        *   `edit(id)`: Show edit form (GET)
        *   `update(id)`: Update resource (POST)
        *   `delete(id)`: Delete resource (POST)

*   **Views**: Located in `app/templates/`.
    *   Organize by feature folder (e.g., `templates/projects/`, `templates/tasks/`).
    *   Reusable components go in `templates/components/`.

## 2. Models
*   **One Class per File**: Models must be defined in separate files within the `app/models/` package.
    *   Example: `app/models/project.py` defines the `Project` class.
    *   Example: `app/models/task.py` defines the `Task` class.
*   **Exposing Models**: All models must be imported in `app/models/__init__.py` to be easily accessible via `from app.models import ...`.

## 3. Database Management

### Migrations
We use **Flask-Migrate** (Alembic) for all schema changes.
*   **DO NOT** use `db.create_all()`. It has been removed.
*   **Location**: Migration scripts must be stored in `database/migrations/`.
*   **Workflow**:
    1.  Modify your model (e.g., in `app/models/project.py`).
    2.  Generate migration: `flask db migrate -m "Description of change"`
    3.  Apply migration: `flask db upgrade`

### Seeders
*   **Location**: Seed scripts must be placed in `database/seeders/`.
*   **Naming**: Use descriptive names, e.g., `seed.py`.
*   **Running**:
    ```bash
    python database/seeders/seed.py
    ```
    *Ensure your seeder adds the project root to `sys.path` to import `app` correctly.*

## 4. Components
*   **Forms**: Reusable form fields should be extracted to `app/templates/components/` (e.g., `project_form.html`) to be shared between `create` and `edit` views.
