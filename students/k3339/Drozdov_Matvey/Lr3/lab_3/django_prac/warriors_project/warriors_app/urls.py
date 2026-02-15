from django.urls import path
from .views import *


app_name = "warriors_app"

from django.urls import path
from .views import *

urlpatterns = [
   path("warriors/professions/", WarriorWithProfessionListAPIView.as_view()),
   path("warriors/skills/", WarriorWithSkillsListAPIView.as_view()),
   path("warriors/<int:id>/", WarriorDetailAPIView.as_view()),
   path("warriors/<int:id>/delete/", WarriorDeleteAPIView.as_view()),
   path("warriors/<int:id>/update/", WarriorUpdateAPIView.as_view()),
]