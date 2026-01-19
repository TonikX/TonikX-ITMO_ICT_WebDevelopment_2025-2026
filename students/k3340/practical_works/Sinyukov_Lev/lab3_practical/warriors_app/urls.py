from django.urls import path

from .views import (
    SkillListAPIView,
    SkillCreateAPIView,
    WarriorListWithProfessionsAPIView,
    WarriorListWithSkillsAPIView,
    WarriorRetrieveFullAPIView,
    WarriorDeleteAPIView,
    WarriorUpdateAPIView,
    ProfessionCreateAPIView,
    WarriorCreateAPIView,
)

urlpatterns = [
    path("skills/", SkillListAPIView.as_view(), name="skills_list"),
    path("skills/create/", SkillCreateAPIView.as_view(), name="skills_create"),

    path("warriors/full/professions/", WarriorListWithProfessionsAPIView.as_view(), name="warriors_with_professions"),
    path("warriors/full/skills/", WarriorListWithSkillsAPIView.as_view(), name="warriors_with_skills"),
    path("warriors/<int:pk>/", WarriorRetrieveFullAPIView.as_view(), name="warrior_full"),
    path("warriors/<int:pk>/delete/", WarriorDeleteAPIView.as_view(), name="warrior_delete"),
    path("warriors/<int:pk>/update/", WarriorUpdateAPIView.as_view(), name="warrior_update"),

    path("professions/create/", ProfessionCreateAPIView.as_view(), name="profession_create"),
    path("warriors/create/", WarriorCreateAPIView.as_view(), name="warrior_create"),
]