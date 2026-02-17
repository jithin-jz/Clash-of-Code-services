from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .utils import generate_refresh_token


class AuthCookieFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cookieuser",
            email="cookie@example.com",
            password="password",
        )

    def test_refresh_accepts_cookie_token(self):
        refresh = generate_refresh_token(self.user)
        self.client.cookies["refresh_token"] = refresh

        response = self.client.post(reverse("refresh_token"), {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("access_token", response.cookies)
