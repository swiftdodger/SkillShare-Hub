from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50)
    instructor = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    content = models.TextField()
    video = models.FileField(upload_to='course_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"