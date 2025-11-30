from rest_framework import serializers
from .models import Room, Client, Employee, CleaningSchedule, Stay
from datetime import date

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class CleaningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = "__all__"


class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = "__all__"

class ClientWithCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "last_name", "first_name", "patronymic", "city"]


class RoomReportSerializer(serializers.Serializer):
    room_number = serializers.CharField()
    clients_count = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=12, decimal_places=2)


class QuarterReportSerializer(serializers.Serializer):
    rooms = RoomReportSerializer(many=True)
    rooms_per_floor = serializers.ListField()
    total_income = serializers.DecimalField(max_digits=14, decimal_places=2)
