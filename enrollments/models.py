from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_enrollment')
        ]

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
