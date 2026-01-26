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
    class Meta:
        model = StayRecord
        fields = '__all__'


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
