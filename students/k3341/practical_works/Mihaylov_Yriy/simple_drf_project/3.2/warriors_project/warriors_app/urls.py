from django.urls import path
from .views import (
    WarriorAPIView,
    ProfessionCreateView,
    SkillListAPIView,
    SkillCreateAPIView,
    WarriorProfessionListAPIView,
    WarriorSkillListAPIView,
    WarriorDetailAPIView,
)

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view(), name='warriors-list'),
    path('profession/create/', ProfessionCreateView.as_view(), name='profession-create'),

    path('skills/', SkillListAPIView.as_view(), name='skills-list'),
    path('skills/create/', SkillCreateAPIView.as_view(), name='skills-create'),

    path('warriors/professions/', WarriorProfessionListAPIView.as_view(), name='warriors-professions'),
    path('warriors/skills/', WarriorSkillListAPIView.as_view(), name='warriors-skills'),
    path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
]