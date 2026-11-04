
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountTests(TestCase):

    # TA-06 / FR-07: Naudotojo registracija
    def test_user_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "StrongTestPass!2026",
                "password2": "StrongTestPass!2026",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            User.objects.filter(username="testuser").exists()
        )

    # TA-07 / FR-08: Registracijos duomenų tikrinimas
    def test_registration_without_email(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "invaliduser",
                "email": "",
                "password1": "StrongTestPass!2026",
                "password2": "StrongTestPass!2026",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="invaliduser").exists()
        )

    # TA-08 / FR-09: Naudotojo prisijungimas
    def test_user_login(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongTestPass!2026"
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "StrongTestPass!2026",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )

    # TA-09 / FR-10: Naudotojo atsijungimas
    def test_user_logout(self):
        User.objects.create_user(
            username="testuser",
            password="StrongTestPass!2026"
        )

        self.client.login(
            username="testuser",
            password="StrongTestPass!2026"
        )

        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )
