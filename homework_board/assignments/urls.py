from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    
    # Задания
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignments/create/', views.AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:pk>/update/', views.AssignmentUpdateView.as_view(), name='assignment_update'),
    path('assignments/<int:pk>/delete/', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
    path('assignments/<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    
    # Оценки
    path('grades/', views.GradeListView.as_view(), name='grade_list'),
    path('grades/submission/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    
    # Студенческие страницы
    path('my-submissions/', views.my_submissions, name='my_submissions'),
    path('profile/', views.profile, name='profile'),
    
    # Статистика
    path('statistics/', views.statistics, name='statistics'),
]
