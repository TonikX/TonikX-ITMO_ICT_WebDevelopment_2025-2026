from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('register/', views.register, name='register'),
    path('grades/', views.grades_table, name='grades_table'),
]