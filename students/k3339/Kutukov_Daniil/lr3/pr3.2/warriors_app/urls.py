from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
    # ========================================================================
    # APIView endpoints (примеры из методички)
    # ========================================================================
    path("api/warriors/", WarriorAPIView.as_view(), name="warrior-api"),
    path(
        "api/profession/create/",
        ProfessionCreateView.as_view(),
        name="profession-create-api",
    ),
    # Практическое задание 1: APIView для Skill
    path("api/skills/", SkillAPIView.as_view(), name="skill-list-api"),
    path("api/skills/create/", SkillCreateAPIView.as_view(), name="skill-create-api"),
    # ========================================================================
    # Generic Views endpoints
    # ========================================================================
    path("warriors/list/", WarriorListAPIView.as_view(), name="warrior-list"),
    path(
        "profession/generic_create/",
        ProfessionCreateAPIView.as_view(),
        name="profession-create",
    ),
    path("skills/list/", SkillListAPIView.as_view(), name="skill-list"),
    path(
        "skills/generic_create/",
        SkillCreateGenericAPIView.as_view(),
        name="skill-create",
    ),
    # ========================================================================
    # Практическое задание: Generic Views с вложенными данными
    # ========================================================================
    # 1. Вывод полной информации о всех воинах и их профессиях
    path(
        "warriors/with-professions/",
        WarriorWithProfessionListAPIView.as_view(),
        name="warrior-with-professions",
    ),
    # 2. Вывод полной информации о всех воинах и их скилах
    path(
        "warriors/with-skills/",
        WarriorWithSkillsListAPIView.as_view(),
        name="warrior-with-skills",
    ),
    # 3. Вывод полной информации о воине (по id), его профессии и скилах
    path("warriors/<int:pk>/", WarriorDetailAPIView.as_view(), name="warrior-detail"),
    # 4. Удаление воина по id
    path(
        "warriors/<int:pk>/delete/",
        WarriorDeleteAPIView.as_view(),
        name="warrior-delete",
    ),
    # 5. Редактирование информации о воине
    path(
        "warriors/<int:pk>/update/",
        WarriorUpdateAPIView.as_view(),
        name="warrior-update",
    ),
    # Бонус: комбинированный endpoint (получение, обновление, удаление)
    path(
        "warriors/<int:pk>/full/",
        WarriorRetrieveUpdateDestroyAPIView.as_view(),
        name="warrior-full",
    ),
]
