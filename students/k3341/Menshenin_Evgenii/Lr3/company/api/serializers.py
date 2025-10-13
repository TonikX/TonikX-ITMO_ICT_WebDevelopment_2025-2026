from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Airport, Company, Plane, Flight, Seat, Passenger, Ticket, CrewMember, Crew
)

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = '__all__'

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'

class MarkAllSerializer(serializers.Serializer):
    mark = serializers.CharField()
    count_boards = serializers.IntegerField()

class MarkTopSerializer(serializers.Serializer):
    top_mark = serializers.CharField()

class AvailableSeatsSerializer(serializers.Serializer):
    available_seats = serializers.ListField(child=serializers.IntegerField())

class PlanesInRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = '__all__'

class EmployeesCountSerializer(serializers.Serializer):
    employees_count = serializers.IntegerField()

class RoutesPickSerializer(serializers.Serializer):
    filled_less_than = serializers.FloatField(required=False)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')