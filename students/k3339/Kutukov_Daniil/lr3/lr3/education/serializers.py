from rest_framework import serializers
from .models import Classroom, Subject, Teacher, Group, Student, Grade, Schedule
from django.db.models import Avg


class ClassroomSerializer(serializers.ModelSerializer):
    """Сериализатор для кабинета"""

    class Meta:
        model = Classroom
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для дисциплины"""

    class Meta:
        model = Subject
        fields = ["id", "name", "hours_per_semester"]


class TeacherSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для преподавателя"""

    class Meta:
        model = Teacher
        fields = "__all__"


class TeacherDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для преподавателя с вложенными данными"""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Teacher
        fields = "__all__"

    def to_representation(self, instance):
        """Для чтения возвращаем вложенные объекты"""
        representation = super().to_representation(instance)
        representation["subjects"] = SubjectSerializer(
            instance.subjects.all(), many=True
        ).data
        if instance.classroom:
            representation["classroom"] = ClassroomSerializer(instance.classroom).data
        return representation


class GroupSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для группы"""

    class Meta:
        model = Group
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для студента"""

    class Meta:
        model = Student
        fields = "__all__"


class StudentDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для студента с информацией о группе"""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = "__all__"

    def to_representation(self, instance):
        """Для чтения возвращаем вложенные объекты"""
        representation = super().to_representation(instance)
        representation["group"] = GroupSerializer(instance.group).data
        return representation


class GradeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для оценки"""

    class Meta:
        model = Grade
        fields = "__all__"


class GradeDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для оценки с информацией о студенте и дисциплине"""

    grade_display = serializers.CharField(source="get_grade_display", read_only=True)

    class Meta:
        model = Grade
        fields = "__all__"

    def to_representation(self, instance):
        """Для чтения возвращаем вложенные объекты"""
        representation = super().to_representation(instance)
        representation["student"] = StudentSerializer(instance.student).data
        representation["subject"] = SubjectSerializer(instance.subject).data
        return representation


class ScheduleSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для расписания"""

    class Meta:
        model = Schedule
        fields = "__all__"


class ScheduleDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для расписания с полной информацией"""

    day_of_week_display = serializers.CharField(
        source="get_day_of_week_display", read_only=True
    )

    class Meta:
        model = Schedule
        fields = "__all__"

    def to_representation(self, instance):
        """Для чтения возвращаем вложенные объекты"""
        representation = super().to_representation(instance)
        representation["group"] = GroupSerializer(instance.group).data
        representation["subject"] = SubjectSerializer(instance.subject).data
        representation["teacher"] = TeacherSerializer(instance.teacher).data
        representation["classroom"] = ClassroomSerializer(instance.classroom).data
        return representation


class GroupDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для группы с информацией о студентах"""

    students = StudentSerializer(many=True, read_only=True)
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"

    def get_students_count(self, obj):
        return obj.students.count()


class GradeSheetSerializer(serializers.Serializer):
    """Сериализатор для ведомости успеваемости группы"""

    group = GroupSerializer(read_only=True)
    semester = serializers.IntegerField()
    students_grades = serializers.SerializerMethodField()
    average_grade = serializers.SerializerMethodField()

    def get_students_grades(self, obj):
        """Получить оценки всех студентов группы"""
        students = obj["group"].students.all()
        semester = obj["semester"]
        result = []

        for student in students:
            grades = Grade.objects.filter(
                student=student, semester=semester
            ).select_related("subject")

            student_data = {
                "student": StudentSerializer(student).data,
                "grades": GradeDetailSerializer(grades, many=True).data,
                "average": grades.aggregate(avg=Avg("grade"))["avg"] or 0,
            }
            result.append(student_data)

        return result

    def get_average_grade(self, obj):
        """Средний балл группы за семестр"""
        grades = Grade.objects.filter(
            student__group=obj["group"], semester=obj["semester"]
        )
        avg = grades.aggregate(avg=Avg("grade"))["avg"]
        return round(avg, 2) if avg else 0


class TeacherGroupsSerializer(serializers.Serializer):
    """Сериализатор для групп, где преподаватель ведет определенный предмет"""

    teacher = TeacherSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
