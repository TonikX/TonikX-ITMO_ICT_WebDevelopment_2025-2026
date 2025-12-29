from django.urls import path
from .views import (
    WarriorListAPIView,
    WarriorCreateAPIView,
    WarriorProfessionListAPIView,
    WarriorSkillListAPIView,
    WarriorRetrieveAPIView,
    WarriorDestroyAPIView,
    WarriorUpdateAPIView,
    ProfessionCreateView,
    SkillCreateView,
    SkillAPIView
)

app_name = "warriors_app"

urlpatterns = [
    # Базовые операции с воинами
    path('warriors/', WarriorListAPIView.as_view(), name='warriors'),
    path('warriors/create/', WarriorCreateAPIView.as_view(), name='warrior_create'),

    # Задание 1: Воины с профессиями
    path('warriors/professions/', WarriorProfessionListAPIView.as_view(), name='warriors_professions'),

    # Задание 2: Воины со скилами
    path('warriors/skills/', WarriorSkillListAPIView.as_view(), name='warriors_skills'),

    # Задание 3: Полная информация о воине по ID
    path('warriors/<int:id>/', WarriorRetrieveAPIView.as_view(), name='warrior_detail'),

    # Задание 4: Удаление воина
    path('warriors/delete/<int:id>/', WarriorDestroyAPIView.as_view(), name='warrior_delete'),

    # Задание 5: Редактирование воина
    path('warriors/update/<int:id>/', WarriorUpdateAPIView.as_view(), name='warrior_update'),

    # Профессии (старые эндпоинты)
    path('profession/create/', ProfessionCreateView.as_view(), name='profession_create'),

    # Скилы (старые эндпоинты)
    path('skills/', SkillAPIView.as_view(), name='skills'),
    path('skill/create/', SkillCreateView.as_view(), name='skill_create'),
]