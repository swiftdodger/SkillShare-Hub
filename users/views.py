from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from users.forms import RegisterForm, UserProfileForm
from users.models import UserProfile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')  # ✅ get selected role from form
            # Create UserProfile and attach the selected role
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('role_redirect')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def root_redirect(request):
    if request.user.is_authenticated:
        role = request.user.userprofile.role
        if role == 'instructor':
            return redirect('instructor_dashboard')
        else:
            return redirect('student_dashboard')
    else:
        return redirect('register')

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def role_redirect(request):
    role = request.user.userprofile.role
    if role == 'instructor':
        return redirect('instructor_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def instructor_dashboard(request):
    if request.user.userprofile.role != 'instructor':
        return render(request, 'unauthorized.html', status=403)
    return render(request, 'instructor_dashboard.html')

@login_required
def student_dashboard(request):
    if request.user.userprofile.role != 'student':
        return render(request, 'unauthorized.html', status=403)
    return render(request, 'student_dashboard.html')
