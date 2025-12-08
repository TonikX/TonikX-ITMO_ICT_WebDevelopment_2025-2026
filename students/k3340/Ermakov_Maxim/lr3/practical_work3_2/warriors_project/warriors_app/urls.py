from django.urls import path
from .views import SkillListAPIView, SkillCreateAPIView, WarriorAPIView,  ProfessionCreateView, WarriorProfessionListAPIView, WarriorSkillListAPIView, WarriorFullDetailView, WarriorDeleteView, WarriorUpdateView # и другие вьюшки по мере добавления

app_name = "warriors_app"

urlpatterns = [
    path('skills/', SkillListAPIView.as_view(), name='skill-list'),
    path('skills/create/', SkillCreateAPIView.as_view(), name='skill-create'),
    path('warriors/', WarriorAPIView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path('warriors/professions/', WarriorProfessionListAPIView.as_view(),
         name='warrior-profession-list'),
    path('warriors/skills/', WarriorSkillListAPIView.as_view(),
         name='warrior-skill-list'),
    path('warriors/<int:id>/full/', WarriorFullDetailView.as_view(),
         name='warrior-full-detail'),
    # 4. Удаление по id
    path('warriors/<int:id>/delete/', WarriorDeleteView.as_view(),
         name='warrior-delete'),
    # 5. Редактирование по id
    path('warriors/<int:id>/update/', WarriorUpdateView.as_view(),
         name='warrior-update'),
]
