from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('homework/', views.homework_list, name='homework_list'),
    path('homework/submit/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    path('grades/', views.grades_table, name='grades_table'),
    path('submission/<int:submission_id>/', views.view_submission, name='view_submission'),
]