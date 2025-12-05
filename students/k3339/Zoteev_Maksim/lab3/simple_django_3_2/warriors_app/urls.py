from django.urls import path
from .views import (
    WarriorAPIView,
    ProfessionCreateView,
    SkillAPIView,
    SkillCreateView,
    WarriorProfessionAPIView,
    WarriorSkillAPIView,
    WarriorDetailAPIView,
)

urlpatterns = [
    path("warriors/", WarriorAPIView.as_view(), name="warriors-list"),
    path("warrior/<int:pk>/", WarriorDetailAPIView.as_view(), name="warrior-detail"),
    path(
        "warriors/professions/",
        WarriorProfessionAPIView.as_view(),
        name="warriors-professions",
    ),
    path("warriors/skills/", WarriorSkillAPIView.as_view(), name="warriors-skills"),
    path(
        "profession/create/", ProfessionCreateView.as_view(), name="profession-create"
    ),
    path("skills/", SkillAPIView.as_view(), name="skills-list"),
    path("skill/create/", SkillCreateView.as_view(), name="skill-create"),
]
