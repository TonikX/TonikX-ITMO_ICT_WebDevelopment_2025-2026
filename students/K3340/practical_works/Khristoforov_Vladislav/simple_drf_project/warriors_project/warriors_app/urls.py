from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('warriors/list/', WarriorListAPIView.as_view()),
   path('warriors/profession/', WarriorProfessionListAPIView.as_view()),
   path('warriors/skill/', WarriorSkillListAPIView.as_view()),
   path('warriors/<int:pk>/', WarriorRetrieveAPIView.as_view()),
   path('warriors/delete/<int:pk>/', WarriorDestroyAPIView.as_view()),
   path('warriors/update/<int:pk>/', WarriorUpdateAPIView.as_view()),
   path('profession/generic_create/', ProfessionCreateAPIView.as_view()),
   path('skills/', SkillAPIView.as_view()),
]