from django.urls import include, path
from rest_framework.routers import DefaultRouter

from school import views

app_name = "school"

router = DefaultRouter()
router.register(r"teachers", views.TeacherViewSet, basename="teacher")
router.register(r"students", views.StudentViewSet, basename="student")
router.register(r"classes", views.SchoolClassViewSet, basename="class")
router.register(r"subjects", views.SubjectViewSet, basename="subject")
router.register(r"classrooms", views.ClassroomViewSet, basename="classroom")
router.register(r"teacher-subjects", views.TeacherSubjectViewSet, basename="teacher-subject")
router.register(
    r"teaching-assignments", views.TeachingAssignmentViewSet, basename="teaching-assignment"
)
router.register(r"grades", views.GradeViewSet, basename="grade")
router.register(r"schedule", views.ScheduleEntryViewSet, basename="schedule")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "analytics/schedule/lookup/",
        views.ScheduleLookupView.as_view(),
        name="schedule-lookup",
    ),
    path(
        "analytics/subjects/teacher-count/",
        views.SubjectTeacherCountView.as_view(),
        name="subject-teacher-count",
    ),
    path(
        "analytics/classes/<int:class_id>/subject-peers/",
        views.SubjectPeersView.as_view(),
        name="subject-peers",
    ),
    path(
        "analytics/classes/gender-distribution/",
        views.GenderDistributionView.as_view(),
        name="gender-distribution",
    ),
    path(
        "analytics/classrooms/categories/",
        views.ClassroomCategoryStatsView.as_view(),
        name="classroom-categories",
    ),
    path(
        "reports/classes/<int:class_id>/",
        views.ClassPerformanceReportView.as_view(),
        name="class-report",
    ),
    path(
        "reports/classes/<int:class_id>/download/",
        views.ClassPerformanceReportDownloadView.as_view(),
        name="class-report-download",
    ),
]

