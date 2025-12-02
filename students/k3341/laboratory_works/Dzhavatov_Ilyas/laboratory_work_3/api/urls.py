from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'schoolclasses', views.SchoolClassViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'classrooms', views.ClassroomViewSet)
router.register(r'grades', views.GradeViewSet)
router.register(r'schedule', views.ScheduleViewSet)
router.register(r'assignments', views.TeachingAssignmentViewSet)
router.register(r'reports', views.ReportViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')), # Эндпоинты Djoser: /auth/users/, /auth/token/login/ и т.д.
    path('auth/', include('djoser.urls.authtoken')), # Для аутентификации по токену
]