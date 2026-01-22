from django.urls import path

from django.urls import include, path
from .views import (
    signup_view, login_view,
    teacher_profile, teacher_records, teacher_subject, teacher_assignments, teacher_assignment_detail, teacher_school_class,
    student_profile, student_records, student_homeworks, student_subject
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),

    path('teacher/profile/', teacher_profile, name="teacher_profile"),
    path('teacher/records/', teacher_records, name="teacher_records"),
    path('teacher/subjects/<int:subject_id>/', teacher_subject, name="teacher_subject"),
    path('teacher/assignments/', teacher_assignments, name="teacher_assignments"),
    path('teacher/assignments/<int:submission_id>/', teacher_assignment_detail, name='teacher_assignment_detail'),
    path('teacher/school_classes/<int:school_class_id>/<int:subject_id>/', teacher_school_class, name='teacher_school_class'),

    path('student/profile/', student_profile, name="student_profile"),
    path('student/records/', student_records, name="student_records"),
    path('student/subjects/<int:subject_id>/', student_subject, name="student_subject"),
    path('student/homework/<int:homework_id>/', student_homeworks, name="student_homeworks"),

]
