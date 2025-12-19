from django.urls import path
from .views import (
    WarriorAPIView,
    ProfessionCreateView,
    ProfessionAPIView,
    SkillAPIView,
    WarriorWithProfessionsView,
    WarriorWithSkillsView,
    WarriorDetailView
)


app_name = "warriors_app"


urlpatterns = [
    # Базовые endpoints
    path('warriors/', WarriorAPIView.as_view(), name='warriors-list'),
    path('profession/create/', ProfessionCreateView.as_view(), name='profession-create'),
    path('professions/', ProfessionAPIView.as_view(), name='professions-list'),
    path('skills/', SkillAPIView.as_view(), name='skills-list'),  # GET + POST

    # Воины с вложенными данными
    path('warriors-with-professions/', WarriorWithProfessionsView.as_view(), name='warriors-with-professions'),
    path('warriors-with-skills/', WarriorWithSkillsView.as_view(), name='warriors-with-skills'),

    # Детальная работа с воином
    path('warrior/<int:warrior_id>/', WarriorDetailView.as_view(), name='warrior-detail'),  # GET, PUT, PATCH, DELETE
]

