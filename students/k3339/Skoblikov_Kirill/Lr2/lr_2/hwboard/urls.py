from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/grades/', views.grade_table, name='grade_table'),
    path('student/active-homeworks/', views.active_homeworks, name='active_homeworks'),
    path('student/profile/', views.student_profile_view, name='student_profile'),
    path('student/submit-homework/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    path('teacher/', views.teacher_page, name='teacher_page'),
]
