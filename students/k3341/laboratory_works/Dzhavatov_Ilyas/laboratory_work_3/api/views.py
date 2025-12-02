from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from core.models import Teacher, Student, SchoolClass, Subject, Classroom, Grade, Schedule, TeachingAssignment
from .serializers import *

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

class TeachingAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TeachingAssignment.objects.all()
    serializer_class = TeachingAssignmentSerializer

class ReportViewSet(viewsets.ViewSet):
    # Кастомные эндпоинты для отчетов

    @action(detail=False, methods=['get'])
    def subject_for_class(self, request):
        """Какой предмет будет в заданном классе, в заданный день недели на заданном уроке?"""
        class_id = request.query_params.get('class_id')
        day = request.query_params.get('day')
        lesson = request.query_params.get('lesson')

        if not all([class_id, day, lesson]):
            return Response({"error": "Необходимы параметры: class_id, day, lesson"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            schedule = Schedule.objects.get(school_class_id=class_id, day_of_week=day, lesson_number=lesson)
            serializer = ScheduleSerializer(schedule)
            return Response(serializer.data)
        except Schedule.DoesNotExist:
            return Response({"detail": "Не найдено."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def teachers_per_subject(self, request):
        """Сколько учителей преподает каждую из дисциплин в школе?"""
        # Группируем назначения по предмету и считаем уникальных учителей
        data = TeachingAssignment.objects.values('subject__name').annotate(teacher_count=Count('teacher', distinct=True)).order_by('subject__name')
        return Response(data)

    @action(detail=False, methods=['get'])
    def same_subject_teachers(self, request):
        """Список учителей, преподающих те же предметы, что и учитель, ведущий информатику в заданном классе."""
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response({"error": "Необходим параметр: class_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Находим предмет "Информатика"
            informatics = Subject.objects.get(name__icontains='информатик')
            # Находим учителей, которые ведут информатику в заданном классе
            target_teachers = TeachingAssignment.objects.filter(subject=informatics, school_class_id=class_id).values_list('teacher', flat=True)
            if not target_teachers:
                return Response({"detail": "В этом классе не найден учитель информатики."}, status=status.HTTP_404_NOT_FOUND)

            # Находим ID предметов, которые ведут эти учителя
            subjects_taught = TeachingAssignment.objects.filter(teacher__in=target_teachers).values_list('subject', flat=True).distinct()
            # Находим всех учителей, которые ведут эти предметы
            teachers = Teacher.objects.filter(teachingassignment__subject__in=subjects_taught).distinct()
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data)
        except Subject.DoesNotExist:
            return Response({"error": "Предмет 'Информатика' не найден в базе."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def gender_count_per_class(self, request):
        """Сколько мальчиков и девочек в каждом классе?"""
        data = Student.objects.values('school_class__name', 'gender').annotate(count=Count('id')).order_by('school_class__name', 'gender')
        # Преобразуем в более удобный формат: { class_name: { 'M': count, 'F': count } }
        result = {}
        for item in data:
            class_name = item['school_class__name']
            if class_name not in result:
                result[class_name] = {'M': 0, 'F': 0}
            result[class_name][item['gender']] = item['count']
        return Response(result)

    @action(detail=False, methods=['get'])
    def classroom_stats(self, request):
        """Сколько кабинетов в школе для базовых и профильных дисциплин?"""
        data = Classroom.objects.values('subject_type').annotate(count=Count('id'))
        return Response(data)

    @action(detail=False, methods=['get'])
    def class_performance_report(self, request):
        """Отчет об успеваемости заданного класса."""
        class_id = request.query_params.get('class_id')
        quarter = request.query_params.get('quarter', 1)  # По умолчанию I четверть
        school_year = request.query_params.get('school_year', '2023-2024')

        if not class_id:
            return Response({"error": "Необходим параметр: class_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            school_class = SchoolClass.objects.get(pk=class_id)
        except SchoolClass.DoesNotExist:
            return Response({"error": "Класс не найден."}, status=status.HTTP_404_NOT_FOUND)

        students = school_class.students.all()
        subjects = Subject.objects.filter(grade__student__in=students, grade__quarter=quarter, grade__school_year=school_year).distinct()

        report_data = {
            'class_name': school_class.name,
            'class_teacher': str(school_class.class_teacher) if school_class.class_teacher else "Не назначен",
            'total_students': students.count(),
            'quarter': quarter,
            'school_year': school_year,
            'subjects': []
        }

        overall_class_grades = []

        for subject in subjects:
            subject_grades = Grade.objects.filter(student__in=students, subject=subject, quarter=quarter, school_year=school_year)
            grade_list = [grade.grade for grade in subject_grades]
            if grade_list:
                avg_grade = sum(grade_list) / len(grade_list)
            else:
                avg_grade = 0
            report_data['subjects'].append({
                'subject_name': subject.name,
                'average_grade': round(avg_grade, 2),
                'grades_count': len(grade_list)
            })
            overall_class_grades.extend(grade_list)

        if overall_class_grades:
            report_data['overall_average_grade'] = round(sum(overall_class_grades) / len(overall_class_grades), 2)
        else:
            report_data['overall_average_grade'] = 0

        return Response(report_data)