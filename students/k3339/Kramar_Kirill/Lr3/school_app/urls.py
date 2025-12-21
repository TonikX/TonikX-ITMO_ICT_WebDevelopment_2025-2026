from django.urls import path

from . import views
from .views import (ClassPerformanceAPIView,
                    SubjectInClassAPIView, TeachersPerSubjectAPIView,
                    TeachersWithSameSubjectsAPIView, GenderCountInClassesAPIView,
                    ClassroomCountAPIView, TeachersViewSet, StudentsViewSet, QuarterGradesViewSet,
                    LessonsViewSet, ClassroomsViewSet, SubjectsViewSet, KlassViewSet, StudentsInClassAPIView
                    )
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="School API",
        default_version='v2',
        description="API for managing school data",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('teachers/', TeachersViewSet.as_view(), name='teachers-list-create'),
    path('teachers/<int:pk>/', TeachersViewSet.as_view(), name='teacher-detail'),

    path('students/', StudentsViewSet.as_view(), name='students-list-create'),
    path('students/<int:pk>/', StudentsViewSet.as_view(), name='student-detail'),

    path('grades/', QuarterGradesViewSet.as_view(), name='grades-list-create'),
    path('grades/<int:pk>/', QuarterGradesViewSet.as_view(), name='grade-detail'),

    path('lessons/', LessonsViewSet.as_view(), name='lessons-list-create'),
    path('lessons/<int:pk>/', LessonsViewSet.as_view(), name='lesson-detail'),

    path('classrooms/', ClassroomsViewSet.as_view(), name='classrooms-list-create'),
    path('classrooms/<int:pk>/', ClassroomsViewSet.as_view(), name='classroom-detail'),

    path('subjects/', SubjectsViewSet.as_view(), name='subjects-list-create'),
    path('subjects/<int:pk>/', SubjectsViewSet.as_view(), name='subject-detail'),

    path('classes/', KlassViewSet.as_view(), name='klasses-list-create'),
    path('classes/<int:pk>/', KlassViewSet.as_view(), name='klass-detail'),
    path('class/<int:klass_id>/performance/', ClassPerformanceAPIView.as_view(), name='class-performance-report'),
    path('class/<int:klass_id>/<str:weekday>/<str:lesson_number>/subject/', SubjectInClassAPIView.as_view(), name='subject-in-class'),
    path('subjects/teachers/count/', TeachersPerSubjectAPIView.as_view(), name='teachers-per-subject'),
    path('teachers/subject/informatics/<int:klass_id>/', TeachersWithSameSubjectsAPIView.as_view(), name='teachers-with-same-subjects'),
    path('classes/gender/count/', GenderCountInClassesAPIView.as_view(), name='gender-count-in-classes'),
    path('classrooms/count/', ClassroomCountAPIView.as_view(), name='classroom-count'),
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('class/<int:klass_id>/students/', StudentsInClassAPIView.as_view(), name='students-in-class'),
    path('class/<int:klass_id>/students/', StudentsInClassAPIView.as_view(), name='students_in_class'),
]
