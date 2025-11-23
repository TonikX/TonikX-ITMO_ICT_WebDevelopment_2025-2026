from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    # ... твои старые пути (skills) ...

    # Задание 1: Воины + Профессии
    path('warriors/profession/', WarriorListProfessionView.as_view()),

    # Задание 2: Воины + Скиллы
    path('warriors/skill/', WarriorListSkillView.as_view()),

    # Задание 3, 4, 5: Детальная инфа, удаление, редактирование
    path('warriors/<int:pk>/', WarriorDetailView.as_view()),
]