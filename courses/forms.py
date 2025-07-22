from django import forms
from courses.models import Course,Lesson

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('instructor', 'created_at')

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video']