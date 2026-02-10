from rest_framework import serializers
from .models import Floor, Room, Client, StayRecord, Employee, CleaningSchedule, CleaningRecord


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'room_type', 'price_per_day')

class FloorDetailSerializer(serializers.ModelSerializer):
    rooms = RoomShortSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = ('id', 'number', 'features', 'rooms')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class StayRecordSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source="room.number", read_only=True)
    client_name = serializers.CharField(
        source="client.first_name", read_only=True
    )
    client_lastname = serializers.CharField(
        source="client.last_name", read_only=True
    )

    class Meta:
        model = StayRecord
        fields = [
            "id",
            "client",
            "client_name",
            "client_lastname",
            "room",
            "room_number",
            "check_in_date",
            "check_out_date",
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class CleaningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = '__all__'


class CleaningRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningRecord
        fields = '__all__'
