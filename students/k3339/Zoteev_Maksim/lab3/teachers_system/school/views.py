from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Avg, Q
from django.shortcuts import get_object_or_404

from .models import (
    Subject, Classroom, Teacher, TeacherSubject, SchoolClass,
    Student, Quarter, TeachingAssignment, Schedule, Grade
)
from .serializers import (
    SubjectSerializer, ClassroomSerializer, TeacherSerializer,
    TeacherDetailSerializer, TeacherSubjectSerializer, SchoolClassSerializer,
    SchoolClassDetailSerializer, StudentSerializer, StudentDetailSerializer,
    QuarterSerializer, TeachingAssignmentSerializer, TeachingAssignmentDetailSerializer,
    ScheduleSerializer, ScheduleDetailSerializer, GradeSerializer,
    GradeCreateUpdateSerializer, ClassGenderStatsSerializer,
    SubjectTeacherCountSerializer, ClassroomTypeCountSerializer,
    ClassPerformanceReportSerializer
)


class SubjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с предметами.
    
    Поддерживает CRUD операции и дополнительные действия:
    - teacher_count: подсчет учителей по каждому предмету
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    @action(detail=False, methods=['get'])
    def teacher_count(self, request):
        """
        Сколько учителей преподает каждую из дисциплин в школе?
        """
        subjects = Subject.objects.annotate(
            teachers_count=Count('teachers', distinct=True)
        ).values('name', 'teachers_count')
        
        result = [
            {'subject': item['name'], 'teachers_count': item['teachers_count']}
            for item in subjects
        ]
        
        serializer = SubjectTeacherCountSerializer(result, many=True)
        return Response(serializer.data)


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с кабинетами.
    
    Поддерживает CRUD операции и дополнительные действия:
    - type_count: подсчет кабинетов по типам
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    
    @action(detail=False, methods=['get'])
    def type_count(self, request):
        """
        Сколько кабинетов в школе для базовых и профильных дисциплин?
        """
        classrooms = Classroom.objects.values('classroom_type').annotate(
            count=Count('id')
        )
        
        result = []
        for item in classrooms:
            type_display = dict(Classroom.CLASSROOM_TYPE_CHOICES).get(
                item['classroom_type'], item['classroom_type']
            )
            result.append({
                'classroom_type': type_display,
                'count': item['count']
            })
        
        serializer = ClassroomTypeCountSerializer(result, many=True)
        return Response(serializer.data)


class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с учителями.
    
    Поддерживает CRUD операции и дополнительные действия:
    - same_subjects: список учителей с теми же предметами
    """
    queryset = Teacher.objects.select_related('classroom').prefetch_related('subjects')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeacherDetailSerializer
        return TeacherSerializer
    
    @action(detail=False, methods=['get'])
    def same_subjects_as_informatics_teacher(self, request):
        """
        Список учителей, преподающих те же предметы, что и учитель информатики в заданном классе.
        
        Query params:
        - class_id: ID класса
        """
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response(
                {'error': 'Параметр class_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Находим назначение преподавания информатики в указанном классе
        informatics_assignment = TeachingAssignment.objects.filter(
            school_class_id=class_id,
            subject__name__icontains='информатик'
        ).first()
        
        if not informatics_assignment:
            return Response(
                {'error': 'Учитель информатики в данном классе не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Получаем предметы этого учителя
        teacher_subjects = informatics_assignment.teacher.subjects.all()
        
        # Находим учителей с теми же предметами
        teachers = Teacher.objects.filter(
            subjects__in=teacher_subjects
        ).exclude(
            id=informatics_assignment.teacher.id
        ).distinct()
        
        serializer = TeacherDetailSerializer(teachers, many=True)
        return Response({
            'informatics_teacher': TeacherDetailSerializer(informatics_assignment.teacher).data,
            'teachers_with_same_subjects': serializer.data
        })


class TeacherSubjectViewSet(viewsets.ModelViewSet):
    """ViewSet для работы со связями учитель-предмет"""
    queryset = TeacherSubject.objects.select_related('teacher', 'subject')
    serializer_class = TeacherSubjectSerializer


class SchoolClassViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с классами.
    
    Поддерживает CRUD операции и дополнительные действия:
    - gender_stats: статистика по полу
    - performance_report: отчет об успеваемости
    """
    queryset = SchoolClass.objects.select_related('class_teacher')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolClassDetailSerializer
        return SchoolClassSerializer
    
    @action(detail=False, methods=['get'])
    def gender_stats(self, request):
        """
        Сколько мальчиков и девочек в каждом классе?
        """
        classes = SchoolClass.objects.annotate(
            boys_count=Count('students', filter=Q(students__gender='M')),
            girls_count=Count('students', filter=Q(students__gender='F')),
            total=Count('students')
        )
        
        result = []
        for school_class in classes:
            result.append({
                'school_class': str(school_class),
                'boys_count': school_class.boys_count,
                'girls_count': school_class.girls_count,
                'total': school_class.total
            })
        
        serializer = ClassGenderStatsSerializer(result, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def performance_report(self, request, pk=None):
        """
        Отчет об успеваемости класса.
        
        Query params:
        - quarter_id: ID четверти (опционально, по умолчанию текущая)
        """
        school_class = self.get_object()
        quarter_id = request.query_params.get('quarter_id')
        
        if quarter_id:
            quarter = get_object_or_404(Quarter, id=quarter_id)
        else:
            quarter = Quarter.objects.filter(is_current=True).first()
            if not quarter:
                return Response(
                    {'error': 'Текущая четверть не найдена'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Получаем студентов класса
        students = school_class.students.all()
        students_count = students.count()
        
        # Получаем оценки за четверть
        grades = Grade.objects.filter(
            student__school_class=school_class,
            quarter=quarter
        ).select_related('subject')
        
        # Средний балл по каждому предмету
        subject_averages = grades.values('subject__name').annotate(
            avg_grade=Avg('value')
        )
        
        average_by_subject = {
            item['subject__name']: round(item['avg_grade'], 2)
            for item in subject_averages
        }
        
        # Общий средний балл по классу
        class_average = grades.aggregate(avg=Avg('value'))['avg']
        class_average = round(class_average, 2) if class_average else 0
        
        # Классный руководитель
        class_teacher_name = (
            school_class.class_teacher.full_name 
            if school_class.class_teacher 
            else 'Не назначен'
        )
        
        result = {
            'school_class': str(school_class),
            'class_teacher': class_teacher_name,
            'students_count': students_count,
            'subjects': list(average_by_subject.keys()),
            'average_by_subject': average_by_subject,
            'class_average': class_average,
            'quarter': str(quarter)
        }
        
        serializer = ClassPerformanceReportSerializer(result)
        return Response(serializer.data)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с учениками.
    
    Поддерживает CRUD операции.
    Фильтрация по классу: ?school_class=1
    """
    queryset = Student.objects.select_related('school_class')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        school_class = self.request.query_params.get('school_class')
        if school_class:
            queryset = queryset.filter(school_class_id=school_class)
        return queryset


class QuarterViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с четвертями"""
    queryset = Quarter.objects.all()
    serializer_class = QuarterSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Получить текущую четверть"""
        quarter = Quarter.objects.filter(is_current=True).first()
        if not quarter:
            return Response(
                {'error': 'Текущая четверть не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(quarter)
        return Response(serializer.data)


class TeachingAssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с назначениями преподавания.
    
    Фильтрация:
    - teacher: по ID учителя
    - school_class: по ID класса
    - quarter: по ID четверти
    """
    queryset = TeachingAssignment.objects.select_related(
        'teacher', 'subject', 'school_class', 'quarter'
    )
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeachingAssignmentDetailSerializer
        return TeachingAssignmentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        teacher = self.request.query_params.get('teacher')
        school_class = self.request.query_params.get('school_class')
        quarter = self.request.query_params.get('quarter')
        
        if teacher:
            queryset = queryset.filter(teacher_id=teacher)
        if school_class:
            queryset = queryset.filter(school_class_id=school_class)
        if quarter:
            queryset = queryset.filter(quarter_id=quarter)
        
        return queryset


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с расписанием.
    
    Поддерживает CRUD операции и дополнительные действия:
    - by_class_day_lesson: предмет в заданном классе, день, урок
    
    Фильтрация:
    - school_class: по ID класса
    - day_of_week: по дню недели (1-6)
    - lesson_number: по номеру урока (1-8)
    """
    queryset = Schedule.objects.select_related(
        'teaching_assignment__teacher',
        'teaching_assignment__subject',
        'teaching_assignment__school_class',
        'classroom'
    )
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScheduleDetailSerializer
        return ScheduleSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        school_class = self.request.query_params.get('school_class')
        day_of_week = self.request.query_params.get('day_of_week')
        lesson_number = self.request.query_params.get('lesson_number')
        
        if school_class:
            queryset = queryset.filter(
                teaching_assignment__school_class_id=school_class
            )
        if day_of_week:
            queryset = queryset.filter(day_of_week=day_of_week)
        if lesson_number:
            queryset = queryset.filter(lesson_number=lesson_number)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_class_day_lesson(self, request):
        """
        Какой предмет будет в заданном классе, в заданный день недели на заданном уроке?
        
        Query params (все обязательные):
        - school_class: ID класса
        - day_of_week: день недели (1-6)
        - lesson_number: номер урока (1-8)
        """
        school_class = request.query_params.get('school_class')
        day_of_week = request.query_params.get('day_of_week')
        lesson_number = request.query_params.get('lesson_number')
        
        if not all([school_class, day_of_week, lesson_number]):
            return Response(
                {'error': 'Параметры school_class, day_of_week и lesson_number обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        schedule = Schedule.objects.filter(
            teaching_assignment__school_class_id=school_class,
            day_of_week=day_of_week,
            lesson_number=lesson_number
        ).select_related(
            'teaching_assignment__subject',
            'teaching_assignment__teacher',
            'classroom'
        ).first()
        
        if not schedule:
            return Response(
                {'message': 'Урок не найден в расписании'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ScheduleDetailSerializer(schedule)
        return Response(serializer.data)


class GradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с оценками.
    
    Фильтрация:
    - student: по ID ученика
    - subject: по ID предмета
    - quarter: по ID четверти
    - school_class: по ID класса
    """
    queryset = Grade.objects.select_related('student', 'subject', 'quarter')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GradeCreateUpdateSerializer
        return GradeSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        student = self.request.query_params.get('student')
        subject = self.request.query_params.get('subject')
        quarter = self.request.query_params.get('quarter')
        school_class = self.request.query_params.get('school_class')
        
        if student:
            queryset = queryset.filter(student_id=student)
        if subject:
            queryset = queryset.filter(subject_id=subject)
        if quarter:
            queryset = queryset.filter(quarter_id=quarter)
        if school_class:
            queryset = queryset.filter(student__school_class_id=school_class)
        
        return queryset
