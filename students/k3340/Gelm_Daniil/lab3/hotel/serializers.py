from rest_framework import serializers
from .models import Room, Guest, Stay, Employee, CleaningSchedule


class RoomSerializer(serializers.ModelSerializer):
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'number', 'room_type', 'room_type_display', 'floor', 'price_per_night', 'phone', 'is_occupied']


class GuestSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Guest
        fields = ['id', 'passport_number', 'last_name', 'first_name', 'middle_name', 'city', 'full_name']


class StaySerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all(), source='guest', write_only=True)
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room', write_only=True)
    
    class Meta:
        model = Stay
        fields = ['id', 'guest', 'guest_id', 'room', 'room_id', 'check_in_date', 'check_out_date']


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'last_name', 'first_name', 'middle_name', 'is_active', 'full_name']


class CleaningScheduleSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), source='employee', write_only=True)
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = CleaningSchedule
        fields = ['id', 'employee', 'employee_id', 'floor', 'day_of_week', 'day_of_week_display']

