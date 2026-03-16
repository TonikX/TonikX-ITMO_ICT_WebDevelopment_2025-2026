from django.urls import path
from . import views

app_name = "warriors_app"

urlpatterns = [
    path('warriors/profession/', views.WarriorProfessionAPIView.as_view()),
    path('warriors/skill/', views.WarriorSkillAPIView.as_view()),
    path('warriors/<int:pk>/', views.WarriorDetailAPIView.as_view()),
    path('warriors/delete/<int:pk>/', views.WarriorDeleteAPIView.as_view()),
    path('warriors/update/<int:pk>/', views.WarriorUpdateAPIView.as_view()),
]