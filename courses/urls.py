from django.urls import path,include
from courses import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('create/', views.create_course,name='create_course'),
    path('list/', views.course_list, name='course_list'),
    path('detail/<int:pk>/', views.course_detail, name='course_detail'),

]