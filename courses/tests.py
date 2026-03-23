from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course

from users.models import UserProfile


class TestCourseViews(TestCase):
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

    def test_unenrolled_student_cannot_open_course_detail(self):
        student = User.objects.create_user(username='student', password='pass123')
        UserProfile.objects.create(user=student, role='student')

        course = Course.objects.create(
            title='Django Advanced',
            description='Views and permissions',
            category='Web',
            instructor=self.user.userprofile,
        )

        self.client.logout()
        self.client.login(username='student', password='pass123')
        response = self.client.get(reverse('course_detail', args=[course.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('course_list'))

