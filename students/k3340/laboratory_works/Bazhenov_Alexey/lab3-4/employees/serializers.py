from rest_framework import serializers

from .models import CleaningAssignment, Employee


class CleaningAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningAssignment
        fields = ['id', 'floor', 'weekday']


class EmployeeSerializer(serializers.ModelSerializer):
    assignments = CleaningAssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'status',
            'hire_date',
            'termination_date',
            'assignments',
        ]


class ScheduleSerializer(serializers.Serializer):
    assignments = CleaningAssignmentSerializer(many=True)

