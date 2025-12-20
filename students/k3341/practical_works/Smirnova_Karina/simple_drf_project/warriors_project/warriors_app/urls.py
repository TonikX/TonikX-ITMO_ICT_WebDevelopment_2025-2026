from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view()),
   path('profession/create/', ProfessionCreateView.as_view()),

   path('skills/', SkillListView.as_view()),
   path('skills/create/', SkillCreateView.as_view()),

   path('warrior/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
   path('warrior/<int:pk>/delete/', WarriorDeleteAPIView.as_view(), name='warrior-delete'),
   path('warrior/<int:pk>/edit/', WarriorUpdateAPIView.as_view(), name='warrior-edit'),
   path('warriors_profession/', WarriorWithProfessionListAPIView.as_view(), name='warriors_profession'),
   path('warriors_skill/', WarriorWithSkillsListAPIView.as_view(), name='warriors_skill'),
]