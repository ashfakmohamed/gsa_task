# GSA Task Scheduler

A Django task scheduling application with authenticated user accounts, private task dashboards, profile details, and optional address geocoding.

## Security

- Passwords are hashed by Django's authentication framework.
- Tasks and profiles are restricted to their owner.
- The Django secret key is supplied through the environment.
- Local databases and virtual environments are excluded from Git.

## Local setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

    python -m pip install -r requirements.txt

3. Set the required environment variables. Copy .env.example and provide a unique DJANGO_SECRET_KEY. Generate one with:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

4. Apply migrations and start the server:

    python manage.py migrate
    python manage.py runserver

5. Open http://127.0.0.1:8000/.

## Tests

    python manage.py test
    python manage.py check
