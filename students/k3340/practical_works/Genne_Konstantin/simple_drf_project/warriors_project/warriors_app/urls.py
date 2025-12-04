from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view()),
   path('profession/create/', ProfessionCreateView.as_view()),
   path('skill/create/', SkillCreateView.as_view()),
   path('skill/', SkillAPIView.as_view()),
   path('warriors/profession/', WarriorWithProfessionAPIView.as_view()),
   path('warriors/skill/', WarriorWithSkillsAPIView.as_view()),
   path('warriors/<int:pk>/skill-and-profession/', WarriorWithProfessionAndSkillsRetrieveAPIView.as_view()),
   path('warriors/<int:pk>/delete', WarriorDestroyAPIView.as_view()),
   path('warriors/<int:pk>/update', WarriorRetrieveUpdateAPIView.as_view())
]