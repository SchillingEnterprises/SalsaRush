# Security Policy

Salsa Rush is a Django event concept and prototype, not a production ticketing, payment, or public user-account platform.

Do not publish security-sensitive details in public issues. Use GitHub private vulnerability reporting when available or contact the maintainer privately.

## Current boundaries

- Only authenticated Django staff accounts can publish events.
- CSRF middleware protects event forms.
- Production startup requires DJANGO_SECRET_KEY; DEBUG is disabled by default.
- The legacy website.User table is not Django authentication. Its password column is retained for database compatibility, marked non-editable, and must never be used for login, registration, or credential storage. Existing values should be treated as sensitive.
- There is no public registration, checkout, or payment-card collection.

Before production, configure a supported application host, production database, HTTPS, private secrets, backups, monitoring, and a suitable privacy notice. Run Django deployment checks in the target environment.

## Tracked development database

The repository includes a tracked SQLite database at `salsaRush/db.sqlite3`. Because this is a public repository, its current contents and historical versions may be accessible to anyone who can read the repository. The database has not been opened or inspected during maintenance. Do not store real customer, attendee, payment, account, or other sensitive records in it. Before any removal or history rewrite, the owner must review its contents and approve a backup, data-retention decision, and repository-history cleanup plan. CI uses a disposable database and verifies that the tracked file's checksum does not change.
