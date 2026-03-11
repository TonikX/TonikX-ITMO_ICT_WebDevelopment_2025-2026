from rest_framework import serializers
from .models import Room, Client, Employee, CleaningSchedule
from django.utils import timezone

class RoomSerializer(serializers.ModelSerializer):
    free = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['id', 'number', 'price', 'room_type', 'floor', 'phone', 'free']

    def get_free(self, obj):
        today = timezone.now().date()
        return not Client.objects.filter(
            room=obj,
            check_in_date__lte=today,
            check_out_date__gte=today
        ).exists()


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