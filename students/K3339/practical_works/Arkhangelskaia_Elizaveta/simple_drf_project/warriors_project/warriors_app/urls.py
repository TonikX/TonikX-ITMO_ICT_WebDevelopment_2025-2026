from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('warriors/professions/', WarriorProfessionAPIView.as_view()),
   path('warriors/skills/', WarriorSkillsAPIView.as_view()),
   path('warriors/list/', WarriorAPIView.as_view()),
   path('warriors/<int:id>/', WarriorDetailAPIView.as_view()),
   path('warriors/<int:id>/delete/', WarriorDestroyAPIView.as_view()),
   path('warriors/<int:id>/update/', WarriorUpdateAPIView.as_view()),
   path('profession/add/', ProfessionCreateView.as_view()),
   path('skills/list/', SkillAPIView.as_view()),
   path('skills/add/', SkillsCreateView.as_view()),
]