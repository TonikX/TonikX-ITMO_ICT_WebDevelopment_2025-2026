from rest_framework import serializers
from .models import Room, Client, Employee, CleaningSchedule

class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class CleaningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = '__all__'


class ClientWithRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    class Meta:
        model = Client
        fields = '__all__'

class CleaningScheduleWithEmployeeSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = CleaningSchedule
        fields = '__all__'