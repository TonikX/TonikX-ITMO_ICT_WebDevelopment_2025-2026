from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('warriors/<int:pk>/', WarriorProfSkillAPIView.as_view()),
    path('warriors/<int:pk>/update/', UpdateWarriorView.as_view()),
    path('warriors/<int:pk>/delete/', DeleteWarriorView.as_view()),
    path('warriors/list/', WarriorListAPIView.as_view()),
    path('warriors/professions/', WarriorProfessionsView.as_view()),
    path('warriors/skills/', WarriorsSkillsView.as_view()),
    path('warriors/create/', WarriorCreateAPIView.as_view(), name='warrior-create'),
    path('skills/', SkillsApiView.as_view()),
    path('warriors/professions/', WarriorWithProfessionListAPIView.as_view(), name='warriors-professions'),
    path('warriors/skills/', WarriorWithSkillsListAPIView.as_view(), name='warriors-skills'),
    path('warriors/<int:id>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
    path('warriors/<int:id>/delete/', WarriorDeleteAPIView.as_view(), name='warrior-delete'),
    path('warriors/<int:id>/update/', WarriorUpdateAPIView.as_view(), name='warrior-update'),
]
