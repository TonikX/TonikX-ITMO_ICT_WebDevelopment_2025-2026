from rest_framework import serializers
from django.db.models import Avg, Count
from .models import (
    Subject, Classroom, Teacher, TeacherSubject, SchoolClass,
    Student, Quarter, TeachingAssignment, Schedule, Grade
)


# ============== БАЗОВЫЕ СЕРИАЛИЗАТОРЫ ==============

class SubjectSerializer(serializers.ModelSerializer):
    """Сериализатор для предмета"""
    subject_type_display = serializers.CharField(
        source='get_subject_type_display', read_only=True
    )
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'subject_type', 'subject_type_display']


class ClassroomSerializer(serializers.ModelSerializer):
    """Сериализатор для кабинета"""
    classroom_type_display = serializers.CharField(
        source='get_classroom_type_display', read_only=True
    )
    
    class Meta:
        model = Classroom
        fields = ['id', 'number', 'classroom_type', 'classroom_type_display', 'description']


class QuarterSerializer(serializers.ModelSerializer):
    """Сериализатор для четверти"""
    number_display = serializers.CharField(
        source='get_number_display', read_only=True
    )
    
    class Meta:
        model = Quarter
        fields = ['id', 'number', 'number_display', 'academic_year', 
                  'start_date', 'end_date', 'is_current']


# ============== СЕРИАЛИЗАТОРЫ УЧИТЕЛЯ ==============

class TeacherSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для учителя"""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'patronymic', 
                  'full_name', 'classroom']


class TeacherDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор учителя с вложенными объектами"""
    full_name = serializers.CharField(read_only=True)
    classroom = ClassroomSerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    supervised_class = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'patronymic', 
                  'full_name', 'classroom', 'subjects', 'supervised_class']
    
    def get_supervised_class(self, obj):
        if hasattr(obj, 'supervised_class'):
            return str(obj.supervised_class)
        return None


class TeacherSubjectSerializer(serializers.ModelSerializer):
    """Сериализатор для связи учитель-предмет"""
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = TeacherSubject
        fields = ['id', 'teacher', 'teacher_name', 'subject', 'subject_name']


# ============== СЕРИАЛИЗАТОРЫ КЛАССА ==============

class SchoolClassSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для класса"""
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = SchoolClass
        fields = ['id', 'number', 'letter', 'name', 'class_teacher']
    
    def get_name(self, obj):
        return str(obj)


class SchoolClassDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор класса с вложенными объектами"""
    name = serializers.SerializerMethodField()
    class_teacher = TeacherSerializer(read_only=True)
    students_count = serializers.SerializerMethodField()
    boys_count = serializers.SerializerMethodField()
    girls_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SchoolClass
        fields = ['id', 'number', 'letter', 'name', 'class_teacher',
                  'students_count', 'boys_count', 'girls_count']
    
    def get_name(self, obj):
        return str(obj)
    
    def get_students_count(self, obj):
        return obj.students.count()
    
    def get_boys_count(self, obj):
        return obj.students.filter(gender='M').count()
    
    def get_girls_count(self, obj):
        return obj.students.filter(gender='F').count()


# ============== СЕРИАЛИЗАТОРЫ УЧЕНИКА ==============

class StudentSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для ученика"""
    gender_display = serializers.CharField(
        source='get_gender_display', read_only=True
    )
    school_class_name = serializers.CharField(
        source='school_class', read_only=True
    )
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 
                  'gender_display', 'school_class', 'school_class_name']


class StudentDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор ученика с вложенными объектами"""
    gender_display = serializers.CharField(
        source='get_gender_display', read_only=True
    )
    school_class = SchoolClassSerializer(read_only=True)
    grades = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 
                  'gender_display', 'school_class', 'grades']
    
    def get_grades(self, obj):
        grades = obj.grades.select_related('subject', 'quarter').all()
        return GradeSerializer(grades, many=True).data


# ============== СЕРИАЛИЗАТОРЫ ОЦЕНКИ ==============

class GradeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для оценки"""
    student_name = serializers.SerializerMethodField()
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    quarter_display = serializers.CharField(source='quarter.__str__', read_only=True)
    
    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_name', 'subject', 'subject_name',
                  'quarter', 'quarter_display', 'value']
    
    def get_student_name(self, obj):
        return f'{obj.student.last_name} {obj.student.first_name}'


class GradeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления оценки"""
    
    class Meta:
        model = Grade
        fields = ['id', 'student', 'subject', 'quarter', 'value']


# ============== СЕРИАЛИЗАТОРЫ НАЗНАЧЕНИЯ ПРЕПОДАВАНИЯ ==============

class TeachingAssignmentSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для назначения преподавания"""
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    school_class_name = serializers.CharField(source='school_class', read_only=True)
    quarter_display = serializers.CharField(source='quarter.__str__', read_only=True)
    
    class Meta:
        model = TeachingAssignment
        fields = ['id', 'teacher', 'teacher_name', 'subject', 'subject_name',
                  'school_class', 'school_class_name', 'quarter', 'quarter_display']


class TeachingAssignmentDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор назначения преподавания"""
    teacher = TeacherSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    school_class = SchoolClassSerializer(read_only=True)
    quarter = QuarterSerializer(read_only=True)
    
    class Meta:
        model = TeachingAssignment
        fields = ['id', 'teacher', 'subject', 'school_class', 'quarter']


# ============== СЕРИАЛИЗАТОРЫ РАСПИСАНИЯ ==============

class ScheduleSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для расписания"""
    day_of_week_display = serializers.CharField(
        source='get_day_of_week_display', read_only=True
    )
    lesson_number_display = serializers.CharField(
        source='get_lesson_number_display', read_only=True
    )
    subject_name = serializers.CharField(
        source='teaching_assignment.subject.name', read_only=True
    )
    teacher_name = serializers.CharField(
        source='teaching_assignment.teacher.full_name', read_only=True
    )
    school_class_name = serializers.CharField(
        source='teaching_assignment.school_class', read_only=True
    )
    classroom_number = serializers.CharField(
        source='classroom.number', read_only=True
    )
    
    class Meta:
        model = Schedule
        fields = ['id', 'teaching_assignment', 'day_of_week', 'day_of_week_display',
                  'lesson_number', 'lesson_number_display', 'classroom', 'classroom_number',
                  'subject_name', 'teacher_name', 'school_class_name']


class ScheduleDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор расписания с вложенными объектами"""
    day_of_week_display = serializers.CharField(
        source='get_day_of_week_display', read_only=True
    )
    lesson_number_display = serializers.CharField(
        source='get_lesson_number_display', read_only=True
    )
    teaching_assignment = TeachingAssignmentDetailSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)
    
    class Meta:
        model = Schedule
        fields = ['id', 'teaching_assignment', 'day_of_week', 'day_of_week_display',
                  'lesson_number', 'lesson_number_display', 'classroom']


# ============== СЕРИАЛИЗАТОРЫ ДЛЯ АНАЛИТИКИ ==============

class ClassGenderStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики по полу в классе"""
    school_class = serializers.CharField()
    boys_count = serializers.IntegerField()
    girls_count = serializers.IntegerField()
    total = serializers.IntegerField()


class SubjectTeacherCountSerializer(serializers.Serializer):
    """Сериализатор для подсчета учителей по предметам"""
    subject = serializers.CharField()
    teachers_count = serializers.IntegerField()


class ClassroomTypeCountSerializer(serializers.Serializer):
    """Сериализатор для подсчета кабинетов по типам"""
    classroom_type = serializers.CharField()
    count = serializers.IntegerField()


class ClassPerformanceReportSerializer(serializers.Serializer):
    """Сериализатор для отчета об успеваемости класса"""
    school_class = serializers.CharField()
    class_teacher = serializers.CharField()
    students_count = serializers.IntegerField()
    subjects = serializers.ListField()
    average_by_subject = serializers.DictField()
    class_average = serializers.FloatField()
    quarter = serializers.CharField()

