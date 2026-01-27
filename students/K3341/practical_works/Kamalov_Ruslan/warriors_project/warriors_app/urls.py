from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
    path('warriors/', WarriorAPIView.as_view(), name='warriors-list'),
    path('profession/create/', ProfessionCreateView.as_view(), name='profession-create'),
    path('skills/', SkillAPIView.as_view(), name='skills-list'),
    path('skills/create/', SkillCreateView.as_view(), name='skill-create'),
    

    path('warriors/professions/', WarriorProfessionListAPIView.as_view(), name='warriors-professions'),    
    path('warriors/skills/', WarriorSkillsListAPIView.as_view(), name='warriors-skills'),
    path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
    path('warriors/<int:pk>/delete/', WarriorDeleteAPIView.as_view(), name='warrior-delete'),
    path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior-update'),
    path('warriors/<int:pk>/manage/', WarriorRetrieveUpdateDestroyAPIView.as_view(), name='warrior-manage'),
]
