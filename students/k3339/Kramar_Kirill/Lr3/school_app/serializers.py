from rest_framework import serializers
from .models import Teacher, Student, QuarterGrade, Lesson, Classroom, Subject, Klass

class KlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = ['id', 'parallel', 'class_number', 'class_teacher']

class StudentSerializer(serializers.ModelSerializer):
    klass = serializers.PrimaryKeyRelatedField(queryset=Klass.objects.all())
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'gender', 'klass']

class QuarterGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterGrade
        fields = "__all__"

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    klass = KlassSerializer()
    classroom = ClassroomSerializer()
    subject = SubjectSerializer(many=True)
    class Meta:
        model = Teacher
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    classroom = ClassroomSerializer()
    subject = SubjectSerializer()
    class Meta:
        model = Lesson
        fields = "__all__"

class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'teacher', 'klass', 'classroom', 'weekday', 'lesson_number']

class TeacherCreateUpdateSerializer(serializers.ModelSerializer):
    klass = serializers.PrimaryKeyRelatedField(queryset=Klass.objects.all())
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True)

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'klass', 'classroom', 'subject']

class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    klass = serializers.PrimaryKeyRelatedField(queryset=Klass.objects.all())

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'gender', 'klass']

class QuarterGradeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterGrade
        fields = ['id', 'student', 'subject', 'grade']

class ClassroomCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'number', 'type']

class SubjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'subject_type']

class KlassCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = ['id', 'parallel', 'class_number', 'class_teacher']
