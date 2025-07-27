from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import UserProfile
# Create your tests here.
class UserRegistrationTests(TestCase):
    def test_register_view_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        data = {
            'username': 'testuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'email': 'test@example.com',
            'role': 'student',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='testuser').exists())