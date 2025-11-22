from django.urls import path
from .views import WarriorAPIView, ProfessionCreateView, SkillAPIView, HomeAPIView
from .views import (
    WarriorProfessionListAPIView,
    WarriorSkillListAPIView,
    WarriorRetrieveAPIView,
    WarriorDestroyAPIView,
    WarriorUpdateAPIView
)
app_name = "warriors_app"

urlpatterns = [
    # Главная страница - корневой путь
    path('', HomeAPIView.as_view(), name='home'),

    # Эндпоинт для просмотра всех воинов
    path('warriors/', WarriorAPIView.as_view(), name='warriors'),

    # Эндпоинт для создания профессий
    path('profession/create/', ProfessionCreateView.as_view(), name='profession-create'),

    # Эндпоинт для просмотра и создания навыков (ПРАКТИЧЕСКОЕ ЗАДАНИЕ)
    path('skills/', SkillAPIView.as_view(), name='skills'),

    # Новые эндпоинты по заданию
    path('warriors/professions/', WarriorProfessionListAPIView.as_view()),
    path('warriors/skills/', WarriorSkillListAPIView.as_view()),
    path('warriors/<int:pk>/', WarriorRetrieveAPIView.as_view()),
    path('warriors/<int:pk>/delete/', WarriorDestroyAPIView.as_view()),
    path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view()),
]