from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course

from users.models import UserProfile

class CourseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='instructor', password='pass123')
        UserProfile.objects.create(user=self.user, role='instructor')
        self.client.login(username='instructor', password='pass123')

    def test_create_course(self):
        data = {
            'title': 'Django Basics',
            'description': 'Intro to Django',
            'category': 'Web',
        }
        response = self.client.post(reverse('create_course'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(title='Django Basics').exists())
