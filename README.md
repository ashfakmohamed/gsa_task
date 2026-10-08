# Django Task Scheduler

<!-- profile-upgrade -->
[![Django CI](https://github.com/ashfakmohamed/django-task-scheduler/actions/workflows/ci.yml/badge.svg)](https://github.com/ashfakmohamed/django-task-scheduler/actions/workflows/ci.yml)

**Stack:** Python · Django · Geocoding

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

## Engineering quality

- GitHub Actions runs Django checks and the automated test suite on every push.
- Runtime configuration is documented through `.env.example`; secrets are not committed.
- Local databases, uploaded media, caches, and virtual environments are excluded from version control.
- Security-sensitive behavior and authorization rules are documented above.