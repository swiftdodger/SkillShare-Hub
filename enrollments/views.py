from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import first

from enrollments.models import Enrollment
from courses.models import Course
# Create your views here.

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if course.instructor == request.user:
        return redirect('course_detail', course.id)

    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('student_dashboard')

@login_required
def unenroll_course(request, course_id):
    enrollement = Enrollment.objects.filter(stundet=request.user, course_id=course_id).first()
    if enrollement:
        enrollement.delete()
    return redirect('student_dashboard')
