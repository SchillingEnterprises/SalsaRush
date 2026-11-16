from datetime import timedelta

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import EventForm
from .models import Event, User as LegacyProfile


class PublicPageTests(TestCase):
    def test_public_pages_render(self):
        for route in ("website:index", "website:about", "website:contact", "website:event_list"):
            with self.subTest(route=route):
                self.assertEqual(self.client.get(reverse(route)).status_code, 200)

    def test_homepage_only_lists_upcoming_events(self):
        upcoming = Event.objects.create(
            title="Friday Salsa Social", description="Music and movement.",
            location="Louisville, KY", date_time=timezone.now() + timedelta(days=5),
        )
        Event.objects.create(
            title="Past Dance Night", location="Louisville, KY",
            date_time=timezone.now() - timedelta(days=5),
        )
        response = self.client.get(reverse("website:index"))
        self.assertContains(response, upcoming.title)
        self.assertNotContains(response, "Past Dance Night")

    def test_event_listing_orders_latest_first(self):
        later = Event.objects.create(
            title="Later Event", location="Louisville",
            date_time=timezone.now() + timedelta(days=10),
        )
        earlier = Event.objects.create(
            title="Earlier Event", location="Louisville",
            date_time=timezone.now() + timedelta(days=2),
        )
        response = self.client.get(reverse("website:event_list"))
        self.assertEqual(list(response.context["events"]), [later, earlier])


class EventManagementTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(
            username="event-manager", email="events@example.test",
            password="a-long-test-only-password", is_staff=True,
        )

    def test_creation_requires_staff_access(self):
        response = self.client.get(reverse("website:event_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_staff_can_create_event(self):
        self.client.force_login(self.staff)
        event_time = (timezone.now() + timedelta(days=14)).strftime("%Y-%m-%dT%H:%M")
        response = self.client.post(reverse("website:event_create"), {
            "title": "Community Dance Night", "description": "A test event.",
            "location": "Louisville, KY", "date_time": event_time,
        })
        self.assertRedirects(response, reverse("website:event_list"))
        self.assertTrue(Event.objects.filter(title="Community Dance Night").exists())

    def test_invalid_event_is_not_saved(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse("website:event_create"), {
            "title": "", "description": "", "location": "", "date_time": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.count(), 0)

    def test_event_form_fields_match_migration_schema(self):
        self.assertEqual(set(EventForm.Meta.fields), {"title", "description", "location", "date_time"})

    def test_csrf_rejects_missing_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.staff)
        client.get(reverse("website:event_create"))
        response = client.post(reverse("website:event_create"), {
            "title": "Must Not Save", "description": "", "location": "Louisville",
            "date_time": (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M"),
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Event.objects.count(), 0)



class LegacyIdentityIsolationTests(TestCase):
    def test_legacy_profile_is_not_the_django_authentication_model(self):
        self.assertIsNot(LegacyProfile, get_user_model())

    def test_legacy_profile_is_not_registered_in_django_admin(self):
        self.assertNotIn(LegacyProfile, admin.site._registry)

    def test_legacy_password_value_is_never_rendered_on_public_pages(self):
        marker = "legacy-profile-secret-must-never-be-rendered"
        LegacyProfile.objects.create(
            username="archive-only-profile",
            password=marker,
            email="legacy-profile@example.test",
            first_name="Legacy",
            last_name="Profile",
        )
        for route in ("website:index", "website:event_list"):
            with self.subTest(route=route):
                self.assertNotContains(self.client.get(reverse(route)), marker)

    def test_legacy_profile_identity_fields_are_not_rendered_on_public_pages(self):
        username = "private-legacy-profile-identifier"
        email = "private-profile-contact@example.test"
        LegacyProfile.objects.create(
            username=username,
            password="unused-legacy-password-value",
            email=email,
            first_name="Private",
            last_name="Profile",
        )
        routes = ("website:index", "website:about", "website:contact", "website:event_list")
        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, username)
                self.assertNotContains(response, email)


class ModelIntegrityTests(TestCase):
    def test_ticket_string_uses_event_title(self):
        from .models import Ticket
        event = Event.objects.create(
            title="Salsa After Dark", location="Louisville, KY",
            date_time=timezone.now() + timedelta(days=1),
        )
        self.assertEqual(str(Ticket.objects.create(event=event, type="General", price="15.00")),
                         "Salsa After Dark - General")

    def test_legacy_password_column_is_non_editable(self):
        from .models import User
        self.assertFalse(User._meta.get_field("password").editable)
