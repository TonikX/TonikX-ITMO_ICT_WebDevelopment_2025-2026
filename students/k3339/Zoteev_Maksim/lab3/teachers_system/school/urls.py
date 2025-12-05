from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubjectViewSet, ClassroomViewSet, TeacherViewSet, TeacherSubjectViewSet,
    SchoolClassViewSet, StudentViewSet, QuarterViewSet,
    TeachingAssignmentViewSet, ScheduleViewSet, GradeViewSet
)

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'teacher-subjects', TeacherSubjectViewSet)
router.register(r'classes', SchoolClassViewSet)
router.register(r'students', StudentViewSet)
router.register(r'quarters', QuarterViewSet)
router.register(r'teaching-assignments', TeachingAssignmentViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'grades', GradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

