from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path('skill/', SkillAPIView.as_view()),
    path('war_info/', WarriorProfessions.as_view()),
    path('war_skill/', WarriorSkills.as_view()),
    path('war_info/<int:pk>/', WarriorPK.as_view()),
]