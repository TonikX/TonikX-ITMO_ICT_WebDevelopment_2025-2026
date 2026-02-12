from datetime import date

from rest_framework import serializers
from django.db.models import Q

from .models import (
    RoomType, Floor, Room, Guest, Stay, Employee, CleaningSchedule
)

class RoomTypeSerializer(serializers.ModelSerializer):
    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Вместимость должна быть больше нуля.")
        return value

    def validate_price_per_day(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена за день должна быть больше нуля.")
        return value

    class Meta:
        model = RoomType
        fields = '__all__'


class FloorSerializer(serializers.ModelSerializer):
    def validate_number(self, value):
        if value <= 0:
            raise serializers.ValidationError("Номер этажа должен быть положительным.")
        return value

    def validate(self, attrs):
        number = attrs.get("number", getattr(self.instance, "number", None))
        if number is not None and Floor.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(number=number).exists():
            raise serializers.ValidationError({"number": "Этаж с таким номером уже существует."})
        return attrs

    class Meta:
        model = Floor
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    type = RoomTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomType.objects.all(), source="type", write_only=True
    )
    floor = FloorSerializer(read_only=True)
    floor_id = serializers.PrimaryKeyRelatedField(
        queryset=Floor.objects.all(), source="floor", write_only=True
    )

    def validate(self, attrs):
        number = attrs.get("number", getattr(self.instance, "number", None))
        floor = attrs.get("floor", getattr(self.instance, "floor", None))

        if not number:
            raise serializers.ValidationError({"number": "Номер комнаты обязателен."})

        if floor and number and Room.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(
            number=number, floor=floor
        ).exists():
            raise serializers.ValidationError({"number": "На этом этаже уже есть комната с таким номером."})

        return attrs

    class Meta:
        model = Room
        fields = ['id', 'number', 'phone', 'type', 'type_id', 'floor', 'floor_id']


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class StaySerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(), source="guest", write_only=True
    )
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source="room", write_only=True
    )

    def validate(self, attrs):
        check_in = attrs.get("check_in", getattr(self.instance, "check_in", None))
        check_out = attrs.get("check_out", getattr(self.instance, "check_out", None))
        room = attrs.get("room", getattr(self.instance, "room", None))

        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError({"check_out": "Дата выезда должна быть позже даты заезда."})

        if check_in and check_in < date.today():
            raise serializers.ValidationError({"check_in": "Дата заезда не может быть в прошлом."})

        if room and check_in and check_out:
            overlapping = Stay.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in,
            )
            if overlapping.exists():
                raise serializers.ValidationError({"room": "Комната занята на выбранные даты."})

        return attrs

    class Meta:
        model = Stay
        fields = ['id', 'check_in', 'check_out', 'guest', 'guest_id', 'room', 'room_id']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class CleaningScheduleSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="employee", write_only=True
    )
    floor = FloorSerializer(read_only=True)
    floor_id = serializers.PrimaryKeyRelatedField(
        queryset=Floor.objects.all(), source="floor", write_only=True
    )
    VALID_WEEKDAYS = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}

    def validate_weekday(self, value):
        if value.lower() not in self.VALID_WEEKDAYS:
            raise serializers.ValidationError("Используйте день недели (например, monday).")
        return value

    def validate(self, attrs):
        weekday = attrs.get("weekday", getattr(self.instance, "weekday", None))
        floor = attrs.get("floor", getattr(self.instance, "floor", None))
        employee = attrs.get("employee", getattr(self.instance, "employee", None))

        if weekday and floor and CleaningSchedule.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(
            weekday__iexact=weekday, floor=floor
        ).exists():
            raise serializers.ValidationError({"weekday": "Для этого этажа уже назначена уборка в этот день."})

        if employee and not employee.employed:
            raise serializers.ValidationError({"employee": "Нельзя назначить уволенного сотрудника."})

        return attrs

    class Meta:
        model = CleaningSchedule
        fields = [
            'id',
            'weekday',
            'employee',
            'employee_id',
            'floor',
            'floor_id',
        ]
