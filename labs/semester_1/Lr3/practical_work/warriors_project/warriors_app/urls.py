from django.urls import path
from .views import (
    WarriorListAPIView, 
    WarriorCreateAPIView,
    WarriorRetrieveAPIView,
    WarriorUpdateAPIView,
    WarriorDestroyAPIView,
    ProfessionListAPIView, 
    ProfessionCreateAPIView,
    ProfessionRetrieveAPIView,
    ProfessionUpdateAPIView,
    ProfessionDestroyAPIView,
    SkillListAPIView, 
    SkillCreateAPIView,
    SkillRetrieveAPIView,
    SkillUpdateAPIView,
    SkillDestroyAPIView,
    WarriorProfessionListAPIView,
    WarriorSkillsListAPIView,
    WarriorProfessionSkillsAPIView,
)

urlpatterns = [
    # Воины
    path('warriors/', WarriorListAPIView.as_view()),
    path('warriors/create/', WarriorCreateAPIView.as_view()),
    path('warriors/<int:pk>/', WarriorRetrieveAPIView.as_view()),
    path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view()),
    path('warriors/<int:pk>/delete/', WarriorDestroyAPIView.as_view()),

    # Профессии
    path('professions/', ProfessionListAPIView.as_view()),
    path('professions/create/', ProfessionCreateAPIView.as_view()),
    path('professions/<int:pk>/', ProfessionRetrieveAPIView.as_view()),
    path('professions/<int:pk>/update/', ProfessionUpdateAPIView.as_view()),
    path('professions/<int:pk>/delete/', ProfessionDestroyAPIView.as_view()),

    # Навыки
    path('skills/', SkillListAPIView.as_view()),
    path('skills/create/', SkillCreateAPIView.as_view()),
    path('skills/<int:pk>/', SkillRetrieveAPIView.as_view()),
    path('skills/<int:pk>/update/', SkillUpdateAPIView.as_view()),
    path('skills/<int:pk>/delete/', SkillDestroyAPIView.as_view()),

    # Специальные запросы
    path('warriors/professions', WarriorProfessionListAPIView.as_view()),
    path('warriors/skills', WarriorSkillsListAPIView.as_view()),
    path('warriors/<int:pk>/detail', WarriorProfessionSkillsAPIView.as_view()),
]
