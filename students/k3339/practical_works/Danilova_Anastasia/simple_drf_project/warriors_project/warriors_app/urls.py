from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('warriors/create/', WarriorCreateAPIView.as_view()),
    path('warriors/list/', WarriorListAPIView.as_view()),
    path('warriors/professions/', WarriorProfessionListAPIView.as_view()),
    path('warriors/skills/', WarriorSkillListAPIView.as_view()),
    path('warriors/<int:id>/', WarriorDetailAPIView.as_view()),
    path('warriors/<int:id>/delete/', WarriorDestroyAPIView.as_view()),
    path('warriors/<int:id>/update/', WarriorUpdateAPIView.as_view()),

    # path('professions/create/', ProfessionCreateView.as_view()),
    path('professions/generic_create/', ProfessionCreateAPIView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    # path('skills/create/', SkillCreateView.as_view()),
    path('skills/generic_create/', SkillCreateAPIView.as_view()),
]
