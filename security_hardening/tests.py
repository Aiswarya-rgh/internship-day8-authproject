from django.core.cache import cache
from rest_framework.test import APITestCase


class SecurityTests(APITestCase):

    def setUp(self):
        cache.clear()

    def test_unauthenticated_profile_access(self):
        response = self.client.get("/api/profile/")

        self.assertIn(response.status_code, [401, 403])

    def test_login_throttling(self):
        url = "/api/login/"

        for _ in range(5):
            self.client.post(
                url,
                {
                    "username": "invalid_user",
                    "password": "wrong_password",
                },
                format="json",
            )

        response = self.client.post(
            url,
            {
                "username": "invalid_user",
                "password": "wrong_password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 429)
