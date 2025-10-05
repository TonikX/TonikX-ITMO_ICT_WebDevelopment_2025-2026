from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('warriors/skills/', WarriorsSkillsView.as_view()),
    path('warriors/professions/', WarriorProfessionsView.as_view()),
    path('warriors/full/', WarriorProfSkillAPIView.as_view()),
    path('warriors/<int:pk>/', WarriorProfSkillAPIView.as_view()),
    path('warriors/<int:pk>/delete/', DeleteWarriorView.as_view()),
    path('warriors/<int:pk>/update/', UpdateWarriorView.as_view()),
    
    path('skills/', SkillsApiView.as_view()),
]
