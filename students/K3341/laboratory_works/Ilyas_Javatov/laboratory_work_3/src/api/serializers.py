from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import (
    Teacher,
    Student,
    SchoolClass,
    Subject,
    Classroom,
    Grade,
    Schedule,
    TeachingAssignment,
)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}
        ref_name = "CustomUserCreate"

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
        ref_name = "CustomUser"


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", "room_number", "subject_type")


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name")


class SchoolClassSerializer(serializers.ModelSerializer):
    class_teacher_name = serializers.CharField(
        source="class_teacher.__str__", read_only=True
    )
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = SchoolClass
        fields = ("id", "name", "class_teacher", "class_teacher_name", "student_count")

    def get_student_count(self, obj):
        return obj.students.count()


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    classroom_number = serializers.CharField(
        source="classroom.room_number", read_only=True
    )
    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=True
    )
    subjects_names = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Teacher
        fields = (
            "id",
            "user",
            "user_id",
            "first_name",
            "last_name",
            "classroom",
            "classroom_number",
            "subjects",
            "subjects_names",
        )


class StudentSerializer(serializers.ModelSerializer):
    school_class_name = serializers.CharField(
        source="school_class.name", read_only=True
    )

    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "gender",
            "school_class",
            "school_class_name",
        )


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.__str__", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = Grade
        fields = (
            "id",
            "student",
            "student_name",
            "subject",
            "subject_name",
            "grade",
            "quarter",
            "school_year",
        )


class ScheduleSerializer(serializers.ModelSerializer):
    school_class_name = serializers.CharField(
        source="school_class.name", read_only=True
    )
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.__str__", read_only=True)
    day_of_week_display = serializers.CharField(
        source="get_day_of_week_display", read_only=True
    )

    class Meta:
        model = Schedule
        fields = (
            "id",
            "school_class",
            "school_class_name",
            "subject",
            "subject_name",
            "teacher",
            "teacher_name",
            "day_of_week",
            "day_of_week_display",
            "lesson_number",
        )

    def validate(self, attrs):
        teacher = attrs.get("teacher", getattr(self.instance, "teacher", None))
        subject = attrs.get("subject", getattr(self.instance, "subject", None))
        school_class = attrs.get(
            "school_class", getattr(self.instance, "school_class", None)
        )
        if teacher and subject and school_class:
            has_assignment = TeachingAssignment.objects.filter(
                teacher=teacher,
                subject=subject,
                school_class=school_class,
            ).exists()
            if not has_assignment:
                raise serializers.ValidationError(
                    "Нельзя поставить в расписание: учитель не назначен на предмет для этого класса."
                )
        return attrs


class TeachingAssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.__str__", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    school_class_name = serializers.CharField(
        source="school_class.name", read_only=True
    )

    class Meta:
        model = TeachingAssignment
        fields = (
            "id",
            "teacher",
            "teacher_name",
            "subject",
            "subject_name",
            "school_class",
            "school_class_name",
            "start_date",
            "end_date",
        )

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError(
                "Дата окончания не может быть раньше даты начала."
            )
        return attrs
