from django.contrib.auth import get_user_model
from django.test import TestCase


class BackendRoutesTests(TestCase):
    def test_root_does_not_serve_the_frontend(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 404)

    def test_current_user_returns_null_when_logged_out(self):
        response = self.client.get("/api/auth/user")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"user": None})

    def test_current_user_returns_authenticated_user(self):
        account = get_user_model().objects.create_user(
            username="navbar-user",
            password="test-password",
        )
        self.client.force_login(account)

        response = self.client.get("/api/auth/user")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"user": {"id": account.id, "username": "navbar-user"}},
        )
