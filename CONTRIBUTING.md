# Contributing

1. Branch from master and keep changes focused.
2. Preserve the existing SQLite database and migration files; never reset them during routine development.
3. Never use the legacy website.User.password column for authentication.
4. Do not commit environment files, secrets, database exports, or personal data.
5. Install dependencies from the repository root: python -m pip install -r requirements.txt
6. From salsaRush/, run:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test website
```

7. Open a pull request with test results and deployment/migration notes.
