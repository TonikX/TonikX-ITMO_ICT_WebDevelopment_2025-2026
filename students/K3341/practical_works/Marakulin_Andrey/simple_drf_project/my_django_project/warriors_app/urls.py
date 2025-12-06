from django.urls import path
from .views import SkillAPIView, SkillCreateView, WarriorProfessionListAPIView, WarriorSkillListAPIView, WarriorRetrieveAPIView, WarriorUpdateAPIView, WarriorDestroyAPIView

app_name = "warriors_app"

urlpatterns = [
    path('skills/', SkillAPIView.as_view(), name='skill_list'),
    path('skills/create/', SkillCreateView.as_view(), name='skill_create'),
    path('warriors/profession_list/', WarriorProfessionListAPIView.as_view(), name='warrior_profession_list'),

    path('warriors/skill_list/', WarriorSkillListAPIView.as_view(), name='warrior_skill_list'),
    path('warriors/<int:pk>/', WarriorRetrieveAPIView.as_view(), name='warrior_detail'),
    path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior_update'),
    path('warriors/<int:pk>/delete/', WarriorDestroyAPIView.as_view(), name='warrior_delete'),
]