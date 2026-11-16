# Salsa Rush

A Django-powered dance and event concept with a public event calendar and staff-managed publishing workflow.

## Current scope

- Responsive homepage and project story.
- Public calendar of listed events.
- Staff-only event creation with validated forms and CSRF protection.
- Django admin event management.
- No public registration, sign-in, payment, or ticket checkout.

This is a prototype, not a live ticketing service. The legacy custom website.User table remains for database compatibility; it is not Django authentication. Its password column is non-editable and must not be used for credentials. See SECURITY.md.

## Requirements

- Python 3.12–3.14
- Django 6.1.3
- Pillow 13.0.0 for existing ImageField models

## Local development

From the repository root:

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install -r requirements.txt
```

Copy .env.example and export the values in your shell or deployment environment. Django does not automatically load .env files.

```bash
cd salsaRush
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/. Django admin is at /admin/. Staff users can publish events at /events/new/.

## Quality checks

From salsaRush/:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test website
```

GitHub Actions runs checks on Python 3.12, 3.13, and 3.14 using a temporary SQLite database. It does not write to the tracked salsaRush/db.sqlite3.

## Hosting

This is a Django application. GitHub Pages can host static HTML/CSS/JavaScript but cannot run the Django backend or database. A production release needs a separate application host, a production database, secrets, HTTPS, backups, and monitoring.

The committed SQLite file and existing migration history have been preserved. CI only migrates its disposable database. Verify event organizers, venues, schedules, images, and any ticket details before presenting an event as active or accepting payment.
