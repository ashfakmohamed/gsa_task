from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Profile, Task


class AuthenticationTests(TestCase):
    @patch("app.views.geocode_address", return_value=(13.08, 80.27))
    def test_registration_hashes_password_and_creates_profile(self, _geocode):
        response = self.client.post(
            reverse("register"),
            {
                "name": "Ashfak",
                "email": "ashfak@example.com",
                "mobile_number": "8525883729",
                "address": "Chennai",
                "password1": "Strong-password-2026!",
                "password2": "Strong-password-2026!",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        user = User.objects.get(username="ashfak@example.com")
        self.assertTrue(user.check_password("Strong-password-2026!"))
        self.assertNotEqual(user.password, "Strong-password-2026!")
        self.assertEqual(user.profile.mobile_number, "8525883729")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("dashboard")}')


class TaskAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="Strong-password-2026!",
        )
        Profile.objects.create(user=self.user, mobile_number="", address="")
        self.other_user = User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="Strong-password-2026!",
        )
        Profile.objects.create(user=self.other_user, mobile_number="", address="")
        today = timezone.localdate()
        Task.objects.create(
            owner=self.user,
            name="My task",
            date=today,
            time=timezone.localtime().time(),
            assigned_to="Ashfak",
        )
        Task.objects.create(
            owner=self.other_user,
            name="Private task",
            date=today,
            time=timezone.localtime().time(),
            assigned_to="Other",
        )
        self.client.force_login(self.user)

    def test_dashboard_only_lists_current_users_tasks(self):
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "My task")
        self.assertNotContains(response, "Private task")

    @patch("app.views.geocode_address", return_value=(None, None))
    def test_created_task_is_owned_by_current_user(self, _geocode):
        scheduled = timezone.localtime() + timedelta(days=1)
        response = self.client.post(
            reverse("task"),
            {
                "name": "Future task",
                "date_time": scheduled.strftime("%Y-%m-%dT%H:%M"),
                "assigned_to": "Ashfak",
                "address": "",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        task = Task.objects.get(name="Future task")
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.status, Task.Status.PENDING)
