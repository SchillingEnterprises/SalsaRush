# Salsa Rush

A Django-powered dance and event concept with a public event calendar and staff-managed publishing workflow.

## Current scope

- Responsive homepage and project story.
- Public calendar of listed events.
- Staff-only event creation with validated forms and CSRF protection.
- Django admin event management.
- No public registration, sign-in, payment, or ticket checkout.

This is a prototype, not a live ticketing service. The legacy custom website.User table remains for database compatibility; it is not Django authentication. Its password column is non-editable and must not be used for credentials. Review the [security policy](SECURITY.md) before configuring or deploying the application.

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

GitHub Actions runs checks on Python 3.12, 3.13, and 3.14 using a temporary SQLite database. The CI sparse checkout excludes the tracked `salsaRush/db.sqlite3` blob; a Git tree-metadata check verifies its object identity is unchanged without opening the file.

## Hosting

This is a Django application. GitHub Pages can host static HTML/CSS/JavaScript but cannot run the Django backend or database. Local development and CI use SQLite only with `DJANGO_DEBUG=true`; non-debug settings reject SQLite. Production must set `DJANGO_DB_ENGINE=postgresql` and provide the database name, user, password, and host. Direct PostgreSQL connections require server-certificate verification (`verify-full` by default, or `verify-ca` for private CA configurations); use `DJANGO_DB_SSLROOTCERT` when the provider requires a custom CA bundle. A production release still needs a separate application host, managed PostgreSQL, secrets, HTTPS, backups, and monitoring.

The committed SQLite file and existing migration history have been preserved. CI only migrates its disposable database. Verify event organizers, venues, schedules, images, and any ticket details before presenting an event as active or accepting payment.


### PostgreSQL deployment configuration

Set `DJANGO_DB_ENGINE=postgresql` and provide `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`, and `DJANGO_DB_HOST`; `DJANGO_DB_PORT` defaults to `5432`. `DJANGO_DB_SSLMODE` defaults to `verify-full` and accepts only `verify-ca` or `verify-full`. `DJANGO_DB_CONN_MAX_AGE` defaults to `60` and is bounded to `0–3600` seconds. Load the password and any CA path from a secret manager; do not commit them. SQLite is permitted only with `DJANGO_DEBUG=true`, and a non-debug process fails closed if PostgreSQL settings are missing. CI runs local tests with a disposable SQLite database in debug mode and a synthetic certificate-verified PostgreSQL configuration for the production deployment check; it never writes to the tracked database.
