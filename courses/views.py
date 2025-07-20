from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course, Lesson
from courses.forms import CourseForm
# Create your views here.

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'detail.html', {'course': course})

@login_required()
def create_course(request):
    if request.user.userprofile.role != 'instructor':
        return redirect('unauthorized')
    if request.method == 'POST':
        form = CourseForm(request.POST,request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})