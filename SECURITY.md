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
