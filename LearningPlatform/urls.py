from django.contrib import admin
from django.urls import path, include
from users.views import root_redirect

urlpatterns = [
    path('', root_redirect, name='root_redirect'),  # default landing page redirecting to role-specific dashboard
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
]