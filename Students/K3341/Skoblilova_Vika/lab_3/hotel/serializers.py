from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Guest, Room, Employee, Booking, CleaningSchedule, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class GuestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Guest
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.last_name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['total_cost', 'booking_date']


class CleaningScheduleSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.last_name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)

    class Meta:
        model = CleaningSchedule
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    booking_info = serializers.CharField(source='booking.id', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'


# Специальные сериализаторы для отчетов
class GuestReportSerializer(serializers.Serializer):
    """Сериализатор для отчета по гостям"""
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    city = serializers.CharField()
    total_bookings = serializers.IntegerField()
    total_days = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)


class RoomReportSerializer(serializers.Serializer):
    """Сериализатор для отчета по номерам"""
    room_number = serializers.CharField()
    room_type = serializers.CharField()
    floor = serializers.IntegerField()
    occupancy_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    bookings_count = serializers.IntegerField()


class EmployeeReportSerializer(serializers.Serializer):
    """Сериализатор для отчета по сотрудникам"""
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    position = serializers.CharField()
    cleaning_count = serializers.IntegerField()
    hire_date = serializers.DateField()

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
