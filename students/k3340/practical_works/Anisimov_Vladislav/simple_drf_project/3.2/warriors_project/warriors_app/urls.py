from django.urls import path
from .views import (
    WarriorListAPIView,
    WarriorCreateAPIView,
    ProfessionCreateAPIView,
    SkillListAPIView,
    SkillCreateAPIView,
    WarriorProfessionListAPIView,
    WarriorSkillListAPIView,
    WarriorRetrieveDestroyAPIView,
    WarriorRetrieveUpdateAPIView,
    SkillOfWarriorCreateAPIView,
)

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorListAPIView.as_view()),
    path('warriors/create/', WarriorCreateAPIView.as_view()),
    path('profession/create/', ProfessionCreateAPIView.as_view()),

    path('skills/', SkillListAPIView.as_view()),
    path('skills/create/', SkillCreateAPIView.as_view()),

    path('warriors/professions/', WarriorProfessionListAPIView.as_view()),
    path('warriors/skills/', WarriorSkillListAPIView.as_view()),
    
    path('warriors/<int:pk>/', WarriorRetrieveDestroyAPIView.as_view()),
    path('warriors/<int:pk>/update/', WarriorRetrieveUpdateAPIView.as_view()),
    
    path('skillofwarrior/create/', SkillOfWarriorCreateAPIView.as_view()),
]