from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"classrooms", views.ClassroomViewSet, basename="classroom")
router.register(r"subjects", views.SubjectViewSet, basename="subject")
router.register(r"teachers", views.TeacherViewSet, basename="teacher")
router.register(r"groups", views.GroupViewSet, basename="group")
router.register(r"students", views.StudentViewSet, basename="student")
router.register(r"grades", views.GradeViewSet, basename="grade")
router.register(r"schedules", views.ScheduleViewSet, basename="schedule")

urlpatterns = [
    path("", include(router.urls)),
]
