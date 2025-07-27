from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from enrollments.models import Enrollment
from courses.models import Course, Lesson
from courses.forms import CourseForm, LessonForm


# Create your views here.

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check access permission
    is_instructor = request.user == course.instructor
    is_enrolled = Enrollment.objects.filter(course=course, student=request.user).exists()

    if not is_instructor and not is_enrolled:
        messages.error(request, "You must enroll to view this course.")
        return redirect('course_list')

    return render(request, 'course_detail.html', {
        'course': course,
        'is_instructor': is_instructor
    })

@login_required()
def create_course(request):
    if request.user.userprofile.role != 'instructor':
        return redirect('unauthorized')
    if request.method == 'POST':
        form = CourseForm(request.POST,request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user.userprofile
            course.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

@login_required()
def lesson_create(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user != course.instructor.user:
        return redirect('unauthorized')

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', course.id)
    else:
        form = LessonForm()
    return render(request, 'lesson_form.html', {'form': form, 'course': course})


@login_required()
def lesson_edit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user != lesson.course.instructor.user:
        return redirect('course_detail', lesson.course.id)

    form = LessonForm(request.POST or None, instance=lesson)
    if form.is_valid():
        form.save()
        return redirect('course_detail', lesson.course.id)
    return render(request, 'lesson_form.html', {'form': form, 'course': lesson.course})

@login_required()
def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user != lesson.course.instructor.user:
        return redirect('course_detail', lesson.course.id)

    if request.method == 'POST':
        lesson.delete()
        return redirect('course_detail', pk=lesson.course.id)

    return render(request, 'lesson_confirm_delete.html', {'lesson': lesson})

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course

    is_instructor = request.user == course.instructor
    is_enrolled = Enrollment.objects.filter(course=course, student=request.user).exists()

    if not is_instructor and not is_enrolled:
        messages.error(request, "Access denied. You must be enrolled to view this lesson.")
        return redirect('course_list')

    return render(request, 'lesson_detail.html', {'lesson': lesson})