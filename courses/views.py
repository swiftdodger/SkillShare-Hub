from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course, Lesson
from courses.forms import CourseForm
# Create your views here.
