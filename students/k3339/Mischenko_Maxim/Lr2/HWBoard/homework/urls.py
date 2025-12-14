from django.urls import path
from django.contrib.auth import logout, views as auth_views
from django.shortcuts import redirect
from . import views

app_name = 'homework'

def logout_view(requst):
    logout(requst)
    return redirect('homework:home')

urlpatterns = [
    path('index/', views.index, name='index'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('grades/', views.grades_table, name='grades_table'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path("register/", views.register, name="register"),
    path('', views.assignment_list, name='home')
]
