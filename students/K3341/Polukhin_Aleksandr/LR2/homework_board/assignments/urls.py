from django.urls import path
from . import views

urlpatterns = [
    # Главная — список всех ДЗ
    path('', views.assignment_list, name='assignment_list'),

    # Детали задания
    path('assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),

    # Регистрация студента
    path('register/', views.register, name='register'),

    # Сдача ДЗ (с выбором или напрямую)
    path('submit/', views.submit_homework, name='submit_homework'),
    path('submit/<int:homework_id>/', views.submit_homework, name='submit_homework'),

    # Мои оценки
    path('grades/', views.grades_table, name='grades_table'),
]