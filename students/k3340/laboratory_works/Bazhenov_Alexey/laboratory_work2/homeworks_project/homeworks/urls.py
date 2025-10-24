from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'homeworks'

urlpatterns = [
    # Главная страница и аутентификация
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='homeworks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Профиль пользователя
    path('profile/', views.profile, name='profile'),
    path('teacher/homework/create/', views.create_homework, name='create_homework'),

    # Просмотр домашних заданий
    path('homeworks/', views.homework_list, name='homework_list'),
    path('homeworks/subject/<int:subject_id>/', views.homework_list_by_subject, name='homework_list_by_subject'),
    path('homework/<int:homework_id>/', views.homework_detail, name='homework_detail'),

    # Сдача домашних заданий
    path('homework/<int:homework_id>/submit/', views.submit_homework, name='submit_homework'),
    path('submission/<int:submission_id>/', views.submission_detail, name='submission_detail'),
    path('submission/<int:submission_id>/edit/', views.edit_submission, name='edit_submission'),

    # Просмотр оценок
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/class/', views.class_grades_table, name='class_grades_table'),
]
