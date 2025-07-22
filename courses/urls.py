from django.urls import path,include
from courses import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('create/', views.create_course,name='create_course'),
    path('list/', views.course_list, name='course_list'),
    path('detail/<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/lessons/new/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:lesson_id>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'),

]