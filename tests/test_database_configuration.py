"""Source contracts for Salsa Rush's local and production database configuration."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DatabaseConfigurationTests(unittest.TestCase):
    def test_sqlite_is_local_default_and_path_can_be_overridden(self):
        settings = (ROOT / "salsaRush/salsaRush/settings.py").read_text(encoding="utf-8")
        self.assertIn('os.environ.get("DJANGO_DB_ENGINE", "sqlite")', settings)
        self.assertIn('os.environ.get("DJANGO_DB_NAME") or str(BASE_DIR / "db.sqlite3")', settings)

    def test_postgresql_requires_all_connection_values(self):
        settings = (ROOT / "salsaRush/salsaRush/settings.py").read_text(encoding="utf-8")
        self.assertIn('django.db.backends.postgresql', settings)
        for name in ("DJANGO_DB_NAME", "DJANGO_DB_USER", "DJANGO_DB_PASSWORD", "DJANGO_DB_HOST"):
            with self.subTest(name=name):
                self.assertIn(name, settings)
        self.assertIn("raise ImproperlyConfigured", settings)

    def test_psycopg_is_in_active_runtime(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("psycopg[binary]==3.3.9", requirements)

    def test_ci_uses_disposable_sqlite_not_tracked_database(self):
        workflow = (ROOT / ".github/workflows/django.yml").read_text(encoding="utf-8")
        self.assertIn("DJANGO_DB_ENGINE: sqlite", workflow)
        self.assertIn("/tmp/salsa-rush-ci.sqlite3", workflow)

    def test_legacy_profile_password_is_not_editable(self):
        models = (ROOT / "salsaRush/website/models.py").read_text(encoding="utf-8")
        self.assertIn('password = models.CharField(max_length=100, editable=False)', models)


if __name__ == "__main__":
    unittest.main(verbosity=2)
