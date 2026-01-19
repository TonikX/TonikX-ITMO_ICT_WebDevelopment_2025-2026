from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet, TaskFileViewSet, TaskLinkViewSet,
    TeamViewSet, TeamMemberViewSet,
    SolutionViewSet, EvaluationViewSet
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'task-files', TaskFileViewSet, basename='taskfile')
router.register(r'task-links', TaskLinkViewSet, basename='tasklink')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'team-members', TeamMemberViewSet, basename='teammember')
router.register(r'solutions', SolutionViewSet, basename='solution')
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')

urlpatterns = [
    path('', include(router.urls)),
]
