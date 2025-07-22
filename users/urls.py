from django.urls import path
from django.contrib.auth import views as auth_views
from users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('redirect-after-login/', views.role_redirect, name='role_redirect'),
    path('dashboard/instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('redirect/', views.role_redirect, name='role_redirect'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
]
