from django.urls import path
from .views import (
    WarriorAPIView, ProfessionCreateView, SkillAPIView,
    WarriorProfessionAPIView, WarriorSkillAPIView, WarriorDetailAPIView
)


app_name = "warriors_app"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view()),
   path('warriors/professions/', WarriorProfessionAPIView.as_view()),
   path('warriors/skills/', WarriorSkillAPIView.as_view()),
   path('warriors/<int:pk>/', WarriorDetailAPIView.as_view()),
   path('profession/create/', ProfessionCreateView.as_view()),
   path('skills/', SkillAPIView.as_view()),
]
