from django.urls import path
from .views import (
    WarriorListAPIView, WarriorProfessionListAPIView,
    WarriorSkillsListAPIView, WarriorDetailAPIView,
    WarriorDeleteAPIView, WarriorUpdateAPIView,
    SkillAPIView, SkillCreateView
)


app_name = "warriors_app"
# url-маршрут — эндпоинт, при обращении к которому сайт будет отдавать данные

urlpatterns = [
    # Скилы через APIView Прописываем сам маршрут в приложении warriors_app и 
    # связываем маршрут с контроллером:
    path('skills/', SkillAPIView.as_view(), name='skill-list'),
    path('skills/create/', SkillCreateView.as_view(), name='skill-create'),
    # Воины через Generic
    path('warriors/', WarriorListAPIView.as_view(), name='warrior-list'),
    path('warriors/professions/', WarriorProfessionListAPIView.as_view(), name='warrior-professions'),
    path('warriors/skills/', WarriorSkillsListAPIView.as_view(), name='warrior-skills'),
    path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
    path('warriors/<int:pk>/delete/', WarriorDeleteAPIView.as_view(), name='warrior-delete'),
    path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior-update'),
]