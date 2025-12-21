from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('submit/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    path('my-grades/', views.my_grades, name='my_grades'),
    path('class-grades/', views.class_grades, name='class_grades'),
]