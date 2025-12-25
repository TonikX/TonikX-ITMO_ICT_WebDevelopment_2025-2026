from django.urls import path
from .views import (
    SkillAPIView, WarriorAPIView, ProfessionCreateView,
    WarriorListAPIView, WarriorCreateAPIView, ProfessionCreateAPIView,
    WarriorWithProfessionListAPIView, WarriorWithSkillsListAPIView,
    WarriorDetailAPIView, WarriorDestroyAPIView, WarriorUpdateAPIView,
    WarriorRetrieveUpdateDestroyAPIView
)

app_name = "warriors_app"

urlpatterns = [
    # APIView endpoints
    path('skills/', SkillAPIView.as_view(), name='skills'),
    path('warriors/', WarriorAPIView.as_view(), name='warriors'),
    path('profession/create/', ProfessionCreateView.as_view(), name='profession_create'),
    
    # Generic API View endpoints
    path('warriors/list/', WarriorListAPIView.as_view(), name='warriors_list'),
    path('warriors/create/', WarriorCreateAPIView.as_view(), name='warriors_create'),
    path('profession/generic_create/', ProfessionCreateAPIView.as_view(), name='profession_generic_create'),
    
    # Полная информация о воинах с профессиями
    path('warriors/with_profession/', WarriorWithProfessionListAPIView.as_view(), name='warriors_with_profession'),
    
    # Полная информация о воинах со скиллами
    path('warriors/with_skills/', WarriorWithSkillsListAPIView.as_view(), name='warriors_with_skills'),
    
    # Полная информация о конкретном воине
    path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior_detail'),
    
    # Удаление воина
    path('warriors/<int:pk>/delete/', WarriorDestroyAPIView.as_view(), name='warrior_delete'),
    
    # Редактирование воина
    path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior_update'),
    
    # Полный CRUD для воина
    path('warriors/<int:pk>/full/', WarriorRetrieveUpdateDestroyAPIView.as_view(), name='warrior_full_crud'),
]
