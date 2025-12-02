from rest_framework import serializers
from .models import Room, Client, Employee, CleaningSchedule, Stay
from datetime import date
from django.db import transaction

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

class CheckInActionSerializer(serializers.Serializer):
    passport_number = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    patronymic = serializers.CharField(
        max_length=50,
        allow_blank=True,
        required=False,
    )
    city = serializers.CharField(max_length=100)

    room_number = serializers.CharField(max_length=10)
    check_in = serializers.DateField()
    check_out = serializers.DateField(required=False, allow_null=True)

    def validate(self, attrs):
        check_in = attrs["check_in"]
        check_out = attrs.get("check_out")
        if check_out is not None and check_out < check_in:
            raise serializers.ValidationError(
                "Дата выезда не может быть раньше даты заселения"
            )
        return attrs


class CheckInResultSerializer(serializers.Serializer):
    client = ClientSerializer()
    room = RoomSerializer()
    stay = StaySerializer()
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)


class ScheduleItemSerializer(serializers.Serializer):
    floor = serializers.IntegerField(min_value=1)
    weekday = serializers.IntegerField(min_value=0, max_value=6)


class HireEmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    patronymic = serializers.CharField(
        max_length=50,
        allow_blank=True,
        required=False,
    )
    is_active = serializers.BooleanField(default=True)
    schedules = ScheduleItemSerializer(many=True)


class HireEmployeeResultSerializer(serializers.Serializer):
    employee = EmployeeSerializer()
    schedules = CleaningScheduleSerializer(many=True)

class RoomWithClientsSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "number",
            "floor",
            "room_type",
            "daily_price",
            "phone_number",
            "clients",
        ]


class ClientWithRoomsSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "last_name",
            "first_name",
            "patronymic",
            "city",
            "rooms",
        ]
