from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('warriors/create/', WarriorCreateAPIView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path('skills/', SkillListAPIView.as_view()),
    path('skills/create/', SkillCreateAPIView.as_view()),
    path('warriors/full/', WarriorProfessionListAPIView.as_view()),
    path('warriors/full_skills/', WarriorSkillListAPIView.as_view()),
    path('warriors/<int:pk>/', WarriorRetrieveAPIView.as_view()),
    path('warriors/<int:pk>/delete/', WarriorDeleteAPIView.as_view()),
    path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view()),
]
