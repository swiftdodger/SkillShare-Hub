from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile
from courses.models import Course
from enrollments.models import Enrollment
from django.urls import reverse

class EnrollmentTests(TestCase):
    def setUp(self):
        # Create student + profile
        self.student_user = User.objects.create_user(username='student', password='pass123')
        self.student_profile = UserProfile.objects.create(user=self.student_user, role='student')

        # Create instructor + profile
        self.instructor_user = User.objects.create_user(username='instructor', password='pass123')
        self.instructor_profile = UserProfile.objects.create(user=self.instructor_user, role='instructor')

        # Create course with UserProfile (not User)
        self.course = Course.objects.create(
            title='Python 101',
            description='Basics of Python',
            category='Programming',
            instructor=self.instructor_profile
        )

    def test_student_can_enroll(self):
        self.client.login(username='student', password='pass123')
        url = reverse('enroll_course', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(student=self.student_user, course=self.course).exists())
