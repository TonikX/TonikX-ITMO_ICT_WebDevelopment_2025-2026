from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Q
from .models import Classroom, Subject, Teacher, Group, Student, Grade, Schedule
from .serializers import *


class ClassroomViewSet(viewsets.ModelViewSet):
    """ViewSet для кабинетов"""

    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class SubjectViewSet(viewsets.ModelViewSet):
    """ViewSet для дисциплин"""

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class TeacherViewSet(viewsets.ModelViewSet):
    """ViewSet для преподавателей"""

    queryset = (
        Teacher.objects.all().select_related("classroom").prefetch_related("subjects")
    )
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherDetailSerializer
    pagination_class = None

    @action(detail=True, methods=["get"])
    def subject_groups(self, request, pk=None):
        """Получить группы, где преподаватель ведет определенный предмет"""
        teacher = self.get_object()
        subject_id = request.query_params.get("subject")

        if not subject_id:
            return Response(
                {"error": "Параметр subject обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response(
                {"error": "Дисциплина не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

        groups = Group.objects.filter(
            schedules__teacher=teacher, schedules__subject=subject
        ).distinct()

        data = {
            "teacher": TeacherSerializer(teacher).data,
            "subject": SubjectSerializer(subject).data,
            "groups": GroupSerializer(groups, many=True).data,
        }

        return Response(data)


class GroupViewSet(viewsets.ModelViewSet):
    """ViewSet для групп"""

    queryset = Group.objects.all().prefetch_related("students")
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GroupDetailSerializer
        return GroupSerializer

    @action(detail=True, methods=["get"])
    def teachers(self, request, pk=None):
        """Получить преподавателей, работающих с группой"""
        group = self.get_object()
        teachers = Teacher.objects.filter(schedules__group=group).distinct()

        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def grade_sheet(self, request, pk=None):
        """Получить ведомость успеваемости группы за семестр"""
        group = self.get_object()
        semester = request.query_params.get("semester")

        if not semester:
            return Response(
                {"error": "Параметр semester обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            semester = int(semester)
            if semester < 1 or semester > 8:
                raise ValueError
        except ValueError:
            return Response(
                {"error": "Семестр должен быть от 1 до 8"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {"group": group, "semester": semester}

        serializer = GradeSheetSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def students_per_course(self, request):
        """Получить количество студентов по курсам"""
        stats = (
            Group.objects.values("course")
            .annotate(students_count=Count("students"))
            .order_by("course")
        )

        return Response(stats)


class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet для студентов"""

    queryset = Student.objects.all().select_related("group")
    permission_classes = [IsAuthenticated]
    serializer_class = StudentDetailSerializer
    pagination_class = None

    @action(detail=True, methods=["get"])
    def grades(self, request, pk=None):
        """Получить оценки студента"""
        student = self.get_object()
        semester = request.query_params.get("semester")

        grades = Grade.objects.filter(student=student)

        if semester:
            grades = grades.filter(semester=semester)

        serializer = GradeDetailSerializer(grades, many=True)
        return Response(serializer.data)


class GradeViewSet(viewsets.ModelViewSet):
    """ViewSet для оценок"""

    queryset = Grade.objects.all().select_related("student", "subject")
    permission_classes = [IsAuthenticated]
    serializer_class = GradeDetailSerializer
    pagination_class = None


class ScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet для расписаний"""

    queryset = Schedule.objects.all().select_related(
        "group", "subject", "teacher", "classroom"
    )
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return ScheduleDetailSerializer
        return ScheduleSerializer

    @action(detail=False, methods=["get"])
    def group_day_schedule(self, request):
        """Получить расписание группы на день"""
        group_id = request.query_params.get("group")
        day = request.query_params.get("day")

        if not group_id or not day:
            return Response(
                {"error": "Параметры group и day обязательны"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            group = Group.objects.get(id=group_id)
            day = int(day)
            if day < 1 or day > 6:
                raise ValueError
        except Group.DoesNotExist:
            return Response(
                {"error": "Группа не найдена"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"error": "День недели должен быть от 1 до 6"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        schedules = Schedule.objects.filter(group=group, day_of_week=day).order_by(
            "lesson_number"
        )

        serializer = ScheduleDetailSerializer(schedules, many=True)
        return Response(
            {
                "group": GroupSerializer(group).data,
                "day_of_week": day,
                "day_name": dict(Schedule.DAYS_OF_WEEK)[day],
                "lessons": serializer.data,
            }
        )

    @action(detail=False, methods=["get"])
    def lesson_info(self, request):
        """Получить информацию о предмете в группе в определенный день на определенном уроке"""
        group_id = request.query_params.get("group")
        day = request.query_params.get("day")
        lesson = request.query_params.get("lesson")

        if not all([group_id, day, lesson]):
            return Response(
                {"error": "Параметры group, day и lesson обязательны"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            schedule = Schedule.objects.get(
                group_id=group_id, day_of_week=int(day), lesson_number=int(lesson)
            )
        except Schedule.DoesNotExist:
            return Response(
                {"error": "Урок не найден в расписании"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError:
            return Response(
                {"error": "Неверный формат параметров"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ScheduleDetailSerializer(schedule)
        return Response(serializer.data)
