from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import serializers
from .models import Flight, Plane, Seat, Passenger, Ticket, CrewMember, Crew, Company, Airport

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
    available_seats = serializers.ListField(child=serializers.CharField())

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
        fields = ('id', 'username', 'email', 'name', 'surname')

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    passenger = serializers.StringRelatedField()
    seat = serializers.StringRelatedField()
    
    class Meta:
        model = Ticket
        fields = ['id', 'passenger', 'seat', 'status', 'sale_channel']

class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = '__all__'

class CrewSerializer(serializers.ModelSerializer):
    member = CrewMemberSerializer(read_only=True)
    
    class Meta:
        model = Crew
        fields = ['id', 'member', 'role', 'medical_check_date', 'medical_status']

class FlightSerializer(serializers.ModelSerializer):
    plane = PlaneSerializer(read_only=True)
    departure_airport = serializers.StringRelatedField()
    destination_airport = serializers.StringRelatedField()
    seats = SeatSerializer(source='seat_set', many=True, read_only=True)
    tickets = TicketSerializer(source='ticket_set', many=True, read_only=True)
    crew = CrewSerializer(source='crew_set', many=True, read_only=True)
    
    class Meta:
        model = Flight
        fields = '__all__'
