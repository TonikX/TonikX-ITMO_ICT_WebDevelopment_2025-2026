from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import (
    Classroom,
    Grade,
    SchoolClass,
    Schedule,
    Student,
    Subject,
    Teacher,
    TeachingAssignment,
)
from .serializers import (
    ClassroomSerializer,
    GradeSerializer,
    ScheduleSerializer,
    SchoolClassSerializer,
    StudentSerializer,
    SubjectSerializer,
    TeacherSerializer,
    TeachingAssignmentSerializer,
)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = (
        Teacher.objects.all()
        .select_related("user", "classroom")
        .prefetch_related("subjects")
    )
    serializer_class = TeacherSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().select_related("school_class")
    serializer_class = StudentSerializer


class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all().select_related("class_teacher")
    serializer_class = SchoolClassSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().select_related("student", "subject")
    serializer_class = GradeSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().select_related(
        "school_class", "subject", "teacher"
    )
    serializer_class = ScheduleSerializer


class TeachingAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TeachingAssignment.objects.all().select_related(
        "teacher", "subject", "school_class"
    )
    serializer_class = TeachingAssignmentSerializer


class ReportViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def subject_for_class(self, request):
        """Какой предмет будет в заданном классе в заданный день и урок."""
        class_id = request.query_params.get("class_id")
        day = request.query_params.get("day")
        lesson = request.query_params.get("lesson")
        if not all([class_id, day, lesson]):
            return Response(
                {"error": "Необходимы параметры: class_id, day, lesson"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        schedule = get_object_or_404(
            Schedule,
            school_class_id=class_id,
            day_of_week=day,
            lesson_number=lesson,
        )
        return Response(ScheduleSerializer(schedule).data)

    @action(detail=False, methods=["get"])
    def teachers_per_subject(self, request):
        """Сколько учителей преподает каждую дисциплину."""
        data = (
            TeachingAssignment.objects.values("subject__name")
            .annotate(teacher_count=Count("teacher", distinct=True))
            .order_by("subject__name")
        )
        return Response(data)

    @action(detail=False, methods=["get"])
    def same_subject_teachers(self, request):
        """Учителя, которые ведут те же предметы, что и учитель информатики в классе."""
        class_id = request.query_params.get("class_id")
        if not class_id:
            return Response(
                {"error": "Необходим параметр: class_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        informatics = get_object_or_404(Subject, name__icontains="информатик")
        target_teachers = TeachingAssignment.objects.filter(
            subject=informatics,
            school_class_id=class_id,
        ).values_list("teacher", flat=True)
        if not target_teachers:
            return Response(
                {"detail": "В этом классе не найден учитель информатики."},
                status=status.HTTP_404_NOT_FOUND,
            )
        subjects_taught = (
            TeachingAssignment.objects.filter(teacher__in=target_teachers)
            .values_list("subject", flat=True)
            .distinct()
        )
        teachers = Teacher.objects.filter(
            teachingassignment__subject__in=subjects_taught
        ).distinct()
        return Response(TeacherSerializer(teachers, many=True).data)

    @action(detail=False, methods=["get"])
    def gender_count_per_class(self, request):
        """Сколько мальчиков и девочек в каждом классе."""
        data = (
            Student.objects.values("school_class__name", "gender")
            .annotate(count=Count("id"))
            .order_by("school_class__name", "gender")
        )
        result = {}
        for item in data:
            class_name = item["school_class__name"]
            result.setdefault(class_name, {"M": 0, "F": 0})
            result[class_name][item["gender"]] = item["count"]
        return Response(result)

    @action(detail=False, methods=["get"])
    def classroom_stats(self, request):
        """Сколько кабинетов для базовых и профильных дисциплин."""
        data = Classroom.objects.values("subject_type").annotate(count=Count("id"))
        return Response(data)

    @action(detail=False, methods=["get"])
    def class_performance_report(self, request):
        """Отчет об успеваемости заданного класса."""
        class_id = request.query_params.get("class_id")
        quarter = request.query_params.get("quarter")
        school_year = request.query_params.get("school_year")
        if not class_id or not quarter or not school_year:
            return Response(
                {"error": "Необходимы параметры: class_id, quarter, school_year"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        school_class = get_object_or_404(SchoolClass, pk=class_id)
        students = school_class.students.all()
        subjects = Subject.objects.filter(
            teachingassignment__school_class=school_class
        ).distinct()
        if not subjects.exists():
            subjects = Subject.objects.filter(
                grade__student__in=students,
                grade__quarter=quarter,
                grade__school_year=school_year,
            ).distinct()

        report_data = {
            "class_name": school_class.name,
            "class_teacher": (
                str(school_class.class_teacher)
                if school_class.class_teacher
                else "Не назначен"
            ),
            "total_students": students.count(),
            "quarter": int(quarter),
            "school_year": school_year,
            "subjects": [],
        }
        overall_class_grades = []
        for subject in subjects:
            subject_grades = Grade.objects.filter(
                student__in=students,
                subject=subject,
                quarter=quarter,
                school_year=school_year,
            )
            grade_list = [grade.grade for grade in subject_grades]
            avg_grade = sum(grade_list) / len(grade_list) if grade_list else 0
            report_data["subjects"].append(
                {
                    "subject_name": subject.name,
                    "average_grade": round(avg_grade, 2),
                    "grades_count": len(grade_list),
                }
            )
            overall_class_grades.extend(grade_list)
        report_data["overall_average_grade"] = (
            round(sum(overall_class_grades) / len(overall_class_grades), 2)
            if overall_class_grades
            else 0
        )
        return Response(report_data)
