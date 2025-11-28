from django.urls import path
from . import views

urlpatterns = [
    path('', views.homework_list, name='homework_list'),
    path('homework/<int:pk>/', views.homework_detail, name='homework_detail'),
    path('homework/<int:pk>/submit/', views.submit_homework, name='submit_homework'),
    path('grades/', views.grades_table, name='grades_table'),
]
