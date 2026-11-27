"""Source contracts for Salsa Rush's local and production database configuration."""
from pathlib import Path
import os
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DatabaseConfigurationTests(unittest.TestCase):
    def test_invalid_boolean_environment_value_fails_closed(self):
        env = os.environ.copy()
        env.update({
            "DJANGO_SETTINGS_MODULE": "salsaRush.settings",
            "DJANGO_SECRET_KEY": "test-only-settings-key",
            "DJANGO_DEBUG": "tru",
            "PYTHONPATH": str(ROOT / "salsaRush"),
        })
        result = subprocess.run(
            [sys.executable, "-c", "from django.conf import settings; print(settings.DEBUG)"],
            cwd=ROOT / "salsaRush",
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_DEBUG must be an explicit boolean value", result.stderr)

    def test_explicit_false_boolean_environment_values_are_supported(self):
        env = os.environ.copy()
        env.update({
            "DJANGO_SETTINGS_MODULE": "salsaRush.settings",
            "DJANGO_SECRET_KEY": "test-only-settings-key",
            "DJANGO_DEBUG": "false",
            "DJANGO_SECURE_SSL_REDIRECT": "off",
            "DJANGO_SESSION_COOKIE_SECURE": "0",
            "DJANGO_CSRF_COOKIE_SECURE": "no",
            "PYTHONPATH": str(ROOT / "salsaRush"),
        })
        result = subprocess.run(
            [sys.executable, "-c", (
                "from django.conf import settings; "
                "assert settings.DEBUG is False; "
                "assert settings.SECURE_SSL_REDIRECT is False; "
                "assert settings.SESSION_COOKIE_SECURE is False; "
                "assert settings.CSRF_COOKIE_SECURE is False"
            )],
            cwd=ROOT / "salsaRush",
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_sqlite_is_local_default_and_path_can_be_overridden(self):
        settings = (ROOT / "salsaRush/salsaRush/settings.py").read_text(encoding="utf-8")
        self.assertIn('os.environ.get("DJANGO_DB_ENGINE", "sqlite")', settings)
        self.assertIn('os.environ.get("DJANGO_DB_NAME") or str(BASE_DIR / "db.sqlite3")', settings)

    def test_secret_key_is_required_even_in_debug_mode(self):
        settings = (ROOT / "salsaRush/salsaRush/settings.py").read_text(encoding="utf-8")
        self.assertIn('SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")', settings)
        self.assertIn('raise ImproperlyConfigured(', settings)
        self.assertNotIn("django-insecure-local-development-only-change-me", settings)

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

    def test_ci_uses_disposable_sqlite_and_excludes_tracked_database_blob(self):
        workflow = (ROOT / ".github/workflows/django.yml").read_text(encoding="utf-8")
        self.assertIn("DJANGO_DB_ENGINE: sqlite", workflow)
        self.assertIn("/tmp/salsa-rush-ci.sqlite3", workflow)
        self.assertIn("sparse-checkout:", workflow)
        self.assertIn("!/salsaRush/db.sqlite3", workflow)
        self.assertIn("sparse-checkout-cone-mode: false", workflow)
        self.assertIn("test ! -e salsaRush/db.sqlite3", workflow)
        self.assertNotIn("sha256sum db.sqlite3", workflow)
        self.assertNotIn("EXPECTED_DATABASE_SHA256", workflow)
        self.assertNotIn("Record tracked database checksum", workflow)

    def test_ci_rejects_changes_to_preserved_database_using_git_metadata(self):
        workflow = (ROOT / ".github/workflows/django.yml").read_text(encoding="utf-8")
        self.assertIn(
            "Ensure the preserved database is unchanged from the base revision",
            workflow,
        )
        self.assertIn(
            'git -C "$GITHUB_WORKSPACE" ls-tree "$comparison_base" -- salsaRush/db.sqlite3',
            workflow,
        )
        self.assertIn(
            'git -C "$GITHUB_WORKSPACE" ls-tree "$GITHUB_SHA" -- salsaRush/db.sqlite3',
            workflow,
        )

    def test_legacy_profile_password_is_not_editable(self):
        models = (ROOT / "salsaRush/website/models.py").read_text(encoding="utf-8")
        self.assertIn('password = models.CharField(max_length=100, editable=False)', models)


if __name__ == "__main__":
    unittest.main(verbosity=2)
