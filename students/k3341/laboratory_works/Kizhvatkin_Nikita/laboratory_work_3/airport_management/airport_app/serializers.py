from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


# Сериализатор для пользователя (регистрация)
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


# Базовые сериализаторы для моделей
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Aircraft
        fields = '__all__'


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


# Сериализатор для сотрудника в составе экипажа
class FlightCrewMemberSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(source='employee.id')
    first_name = serializers.CharField(source='employee.first_name')
    last_name = serializers.CharField(source='employee.last_name')
    position = serializers.CharField(source='employee.position')
    position_display = serializers.CharField(source='employee.get_position_display')
    age = serializers.IntegerField(source='employee.age')
    experience = serializers.IntegerField(source='employee.experience')
    
    class Meta:
        model = CrewMember
        fields = [
            'id', 'employee_id', 'first_name', 'last_name', 'full_name',
            'position', 'position_display', 'age', 'experience',
        ]
    
    def get_full_name(self, obj):
        return f"{obj.employee.last_name} {obj.employee.first_name}"


class EmployeeSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    position_display = serializers.CharField(source='get_position_display', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


class CrewSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Crew
        fields = '__all__'


class CrewMemberSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.__str__', read_only=True)
    employee_position = serializers.CharField(source='employee.position', read_only=True)
    crew_name = serializers.CharField(source='crew.name', read_only=True)

    class Meta:
        model = CrewMember
        fields = '__all__'


class TransitStopSerializer(serializers.ModelSerializer):
    airport_code = serializers.CharField(source='airport.code', read_only=True)
    airport_name = serializers.CharField(source='airport.name', read_only=True)

    class Meta:
        model = TransitStop
        fields = '__all__'


# Сериализатор для полета с полным списком экипажа
class FlightSerializer(serializers.ModelSerializer):
    departure_airport_name = serializers.CharField(source='departure_airport.name', read_only=True)
    departure_airport_code = serializers.CharField(source='departure_airport.code', read_only=True)

    arrival_airport_name = serializers.CharField(source='arrival_airport.name', read_only=True)
    arrival_airport_code = serializers.CharField(source='arrival_airport.code', read_only=True)

    aircraft_tail_number = serializers.CharField(source='aircraft.tail_number', read_only=True)
    aircraft_type = serializers.CharField(source='aircraft.aircraft_type', read_only=True)
    aircraft_capacity = serializers.IntegerField(source='aircraft.capacity', read_only=True)

    company_name = serializers.CharField(source='aircraft.company.name', read_only=True)

    # Полный список экипажа
    crew_members = serializers.SerializerMethodField()

    # Транзитные остановки
    transit_stops = TransitStopSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'distance',
            'departure_airport', 'departure_airport_name', 'departure_airport_code',
            'arrival_airport', 'arrival_airport_name', 'arrival_airport_code',
            'departure_datetime', 'arrival_datetime',
            'aircraft', 'aircraft_tail_number', 'aircraft_type', 'aircraft_capacity',
            'company_name',
            'tickets_sold', 'crew',
            'crew_members',
            'transit_stops'
        ]

    def get_crew_members(self, obj):
        """Полный список всех членов экипажа с детальной информацией"""
        if not obj.crew:
            return []
        
        members = obj.crew.members.all()
        serializer = FlightCrewMemberSerializer(members, many=True)
        return serializer.data


# Сериализатор для отчетов
class AircraftReportSerializer(serializers.Serializer):
    aircraft_type = serializers.CharField()
    count = serializers.IntegerField()
    total_capacity = serializers.IntegerField()
    avg_speed = serializers.FloatField()
    active_count = serializers.IntegerField()
    inactive_count = serializers.IntegerField()
