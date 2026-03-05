from django.urls import path
from warriors_app.views import ProfessionCreateView
from warriors_app.views import SkillAPIView, SkillCreateView
from warriors_app.views import WarriorsAPIView
from warriors_app.views import WarriorProfessionAPIView

from warriors_app.views import WarriorSkillsAPIView, WarriorAPIView, WarriorDeleteView, WarriorUpdateView


app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorsAPIView.as_view()),
    path('warriors/<int:id>/', WarriorAPIView.as_view()),
    path('warriors/<int:id>/delete/', WarriorDeleteView.as_view()),
    path('warriors/<int:id>/update/', WarriorUpdateView.as_view()),
    path('warriors/professions', WarriorProfessionAPIView.as_view()),
    path('warriors/skills', WarriorSkillsAPIView.as_view()),
    path('professions/create', ProfessionCreateView.as_view()),
    path('skills/create', SkillCreateView.as_view()),
    path('skills/', SkillAPIView.as_view())
]
