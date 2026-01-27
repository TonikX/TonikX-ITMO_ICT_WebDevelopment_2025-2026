from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('skills/', SkillAPIView.as_view()),
   path('warrior/<int:pk>', WarriorFullByIdAPIView.as_view()),
   path('warriors/professions', WarriorWithProffesionAPIView.as_view()),
   path('warriors/skills', WarriorWithSkillsAPIView.as_view()),
   path('warrior/<int:pk>/delete', WarriorDeleteAPIView.as_view()),
   path('warrior/<int:pk>/update', WarriorUpdateAPIView.as_view()),
   path('warrior/create', WarriorCreateAPIView.as_view()),
   path('profession/create', ProfessionCreateAPIView.as_view())
]