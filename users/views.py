from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from users.forms import RegisterForm, UserProfileForm
from users.models import UserProfile
from django.contrib.auth.views import LoginView

def register(request):
    if request.user.is_authenticated:
        return redirect('role_redirect')  # If the user is already authenticated, redirect to the role-specific dashboard

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            role = form.cleaned_data.get('role')
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': role}
            )

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('role_redirect')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'


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
