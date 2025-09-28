from django.urls import path
from . import views

urlpatterns = [
    path('', views.homework_list, name='homework_list'),
    path('homework/<int:pk>/', views.homework_detail, name='homework_detail'),
    path('homework/<int:pk>/submit/', views.submit_homework, name='submit_homework'),
    path('student-grades/', views.students_grades_table, name='student_grades_table'),
]