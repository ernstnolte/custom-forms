from django.test import TestCase


class RootPageTests(TestCase):
    def test_root_returns_an_empty_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<body></body>", html=True)
