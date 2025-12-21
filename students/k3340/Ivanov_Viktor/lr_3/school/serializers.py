from typing import Any, Dict

from rest_framework import serializers

from school import models


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classroom
        fields = (
            "id",
            "number",
            "title",
            "category",
            "capacity",
            "created_at",
            "updated_at",
        )


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ("id", "code", "name", "category", "description")


class SchoolClassSerializer(serializers.ModelSerializer):
    homeroom_teacher_name = serializers.CharField(
        source="homeroom_teacher.full_name", read_only=True
    )

    class Meta:
        model = models.SchoolClass
        fields = (
            "id",
            "title",
            "grade_level",
            "profile",
            "homeroom_teacher",
            "homeroom_teacher_name",
            "created_at",
            "updated_at",
        )


class TeacherSubjectSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = models.TeacherSubject
        fields = (
            "id",
            "subject",
            "subject_name",
            "period_start",
            "period_end",
            "hours_per_week",
        )


class TeachingAssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.full_name", read_only=True)
    class_title = serializers.CharField(source="school_class.title", read_only=True)

    class Meta:
        model = models.TeachingAssignment
        fields = (
            "id",
            "teacher",
            "teacher_name",
            "subject",
            "subject_name",
            "school_class",
            "class_title",
            "period_start",
            "period_end",
            "notes",
        )


class TeacherSerializer(serializers.ModelSerializer):
    assigned_room = ClassroomSerializer(read_only=True)
    assigned_room_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Classroom.objects.all(),
        source="assigned_room",
        write_only=True,
        required=False,
        allow_null=True,
    )
    subjects = SubjectSerializer(read_only=True, many=True)
    subject_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Subject.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = models.Teacher
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone",
            "date_of_birth",
            "hired_at",
            "assigned_room",
            "assigned_room_id",
            "subjects",
            "subject_ids",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data: Dict[str, Any]) -> models.Teacher:
        subjects = validated_data.pop("subject_ids", [])
        teacher = super().create(validated_data)
        if subjects:
            teacher.subjects.set(subjects)
        return teacher

    def update(self, instance: models.Teacher, validated_data: Dict[str, Any]) -> models.Teacher:
        subjects = validated_data.pop("subject_ids", None)
        teacher = super().update(instance, validated_data)
        if subjects is not None:
            teacher.subjects.set(subjects)
        return teacher


class StudentSerializer(serializers.ModelSerializer):
    class_title = serializers.CharField(source="school_class.title", read_only=True)

    class Meta:
        model = models.Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "gender",
            "school_class",
            "class_title",
            "date_of_birth",
            "enrollment_date",
            "is_active",
            "created_at",
            "updated_at",
        )


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = models.Grade
        fields = (
            "id",
            "student",
            "student_name",
            "subject",
            "subject_name",
            "quarter",
            "value",
            "comment",
            "graded_by",
            "created_at",
            "updated_at",
        )


class ScheduleEntrySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.full_name", read_only=True)
    class_title = serializers.CharField(source="school_class.title", read_only=True)
    room_number = serializers.CharField(source="room.number", read_only=True)

    class Meta:
        model = models.ScheduleEntry
        fields = (
            "id",
            "school_class",
            "class_title",
            "subject",
            "subject_name",
            "teacher",
            "teacher_name",
            "room",
            "room_number",
            "weekday",
            "lesson_number",
            "starts_at",
            "ends_at",
            "created_at",
            "updated_at",
        )


class ScheduleLookupSerializer(serializers.Serializer):
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=models.SchoolClass.objects.all(), source="school_class"
    )
    weekday = serializers.ChoiceField(choices=models.WeekDay.choices)
    lesson_number = serializers.IntegerField(min_value=1, max_value=10)


class SubjectPeersQuerySerializer(serializers.Serializer):
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=models.SchoolClass.objects.all(), source="school_class"
    )
    subject_code = serializers.CharField(
        required=False,
        help_text="Код предмета (по умолчанию INF).",
    )


class ClassReportRequestSerializer(serializers.Serializer):
    quarter = serializers.ChoiceField(
        choices=models.Quarter.choices, required=False, allow_null=True
    )

