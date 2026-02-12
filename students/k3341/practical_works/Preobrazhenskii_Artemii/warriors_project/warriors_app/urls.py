from django.urls import path

from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/list/', WarriorListAPIView.as_view(), name='warriors_list'),
    path('warriors/create/', WarriorCreateAPIView.as_view(), name='warriors-create'),
    path("warriors/professions/", WarriorWithProfessionListView.as_view(), name="warrior-professions"),
    path("warriors/skills/", WarriorWithSkillsListView.as_view(), name="warrior-skills"),
    path("warrior/<int:id>/", WarriorFullDetailView.as_view(), name="warrior-detail"),
    path("warrior/<int:id>/delete/", WarriorDeleteView.as_view(), name="warrior-delete"),
    path("warrior/<int:id>/update/", WarriorUpdateView.as_view(), name="warrior-update"),
    path('warrior/<int:pk>/add_skill/', AddSkillToWarriorView.as_view(), name='warrior-add-skill'),
    path('profession/create/', ProfessionCreateAPIView.as_view(), name='profession_create'),
    path('profession/list/', ProfessionListAPIView.as_view(), name='profession-list'),
    path('skills/list/', SkillAPIView.as_view(), name='skills_list'),
]