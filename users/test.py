# users/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, Role

class UserTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Test Role", description="Role for testing.")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword",
            role=self.role
        )

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_profile_view(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_edit_profile(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Updated Name',
            'last_name': 'Updated Surname',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated Name')
