from django.test import TestCase
from django.contrib.auth.models import User
from courses.models import Course
from enrollments.models import Enrollment
from django.urls import reverse

# Create your tests here.

class EnrollmentTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='student', password='pass123')
        self.instructor = User.objects.create_user(username='instructor', password='pass123')
        self.course = Course.objects.create(
            title='Python 101',
            description='Basics of Python',
            category='Programming',
            instructor=self.instructor
        )

    def test_student_can_enroll(self):
        self.client.login(username='student', password='pass123')
        url = reverse('enroll_course', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())
