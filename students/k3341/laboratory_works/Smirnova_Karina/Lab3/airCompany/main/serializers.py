from datetime import datetime

from rest_framework import serializers
from .models import AirlineCompany, Plane, Crew, CrewMember, Route, Flight

class AirlineCompanySerializer(serializers.ModelSerializer):
    """
    Простой сериализатор для модели AirlineCompany.
    """
    class Meta:
        model = AirlineCompany
        fields = '__all__'

class PlaneSerializer(serializers.ModelSerializer):
    """
    Простой сериализатор для модели Plane.
    """
    class Meta:
        model = Plane
        fields = '__all__'

class PlaneWithCompanySerializer(serializers.ModelSerializer):
    airline_company = AirlineCompanySerializer()

    class Meta:
        model = Plane
        fields = ['id', 'number', 'type', 'seats_capacity', 'flight_speed', 'in_repair', 'airline_company']

class CrewSerializer(serializers.ModelSerializer):
    """
    Простой сериализатор для модели Crew.
    """
    class Meta:
        model = Crew
        fields = '__all__'

class CrewMemberSerializer(serializers.ModelSerializer):
    """
    Простой сериализатор для модели CrewMember.
    """

    company = AirlineCompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=AirlineCompany.objects.all(),
        write_only=True,
        source='company'
    )
    class Meta:
        model = CrewMember
        fields = [
            'id', 'full_name', 'age', 'education', 'work_experience',
            'passport_info', 'flight_authorization', 'position', 'company', 'company_id'
        ]
class RouteSerializer(serializers.ModelSerializer):
    """
    Простой сериализатор для модели Route.
    """
    class Meta:
        model = Route
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    """
    Простой сериализатор для модели Flight.
    """
    departure_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%d %H:%M'])
    arrival_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%d %H:%M'])

    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'route', 'departure_point', 'arrival_point',
            'departure_datetime', 'arrival_datetime', 'sold_tickets', 'plane', 'crew', 'is_transit'
        ]

# Сериализаторы со связями

class CrewAndMembersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Crew + вложенные члены экипажа.
    """
    members = CrewMemberSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CrewMember.objects.all(), write_only=True, source='members', required=False
    )

    # company = AirlineCompanySerializer(read_only=True)
    # company_id = serializers.PrimaryKeyRelatedField(
    #     queryset=AirlineCompany.objects.all(), write_only=True, required=False, source='company'
    # )

    class Meta:
        model = Crew
        fields = ['id', 'members', 'member_ids']

class FlightInRouteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Flight внутри Route (только основные поля и самолет).
    """
    plane = PlaneSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'departure_point', 'arrival_point',
            'departure_datetime', 'arrival_datetime', 'plane', 'is_transit'
        ]

class RouteWithFlightsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Route + вложенные рейсы.
    """
    flights = FlightInRouteSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = [
            'id', 'departure_point', 'destination_point', 'distance', 'landing_points', 'flights'
        ]

class AirlineCompanyAndPlanesAndCrewMembersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для AirlineCompany + вложенные самолеты и члены экипажа.
    """
    planes = PlaneSerializer(many=True, read_only=True, source='plane_set')
    crew_members = CrewMemberSerializer(many=True, read_only=True)

    class Meta:
        model = AirlineCompany
        fields = ['id', 'name', 'planes', 'crew_members']

class FlightInPlaneSerializer(serializers.ModelSerializer):
    """
    Небольшой сериализатор для рейса внутри объекта Самолёта.
    """
    departure_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%d %H:%M'])
    arrival_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%d %H:%M'])
    route = RouteSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'route', 'departure_point', 'arrival_point',
            'departure_datetime', 'arrival_datetime', 'sold_tickets', 'is_transit'
        ]

class PlaneWithFlightsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Самолёта с вложенным списком рейсов (flight_set).
    """
    flights = FlightInPlaneSerializer(many=True, read_only=True, source='flight_set')
    airline_company = AirlineCompanySerializer(read_only=True)

    class Meta:
        model = Plane
        fields = ['id', 'number', 'type', 'seats_capacity', 'flight_speed', 'in_repair', 'airline_company', 'flights']

class FlightEverythingSerializer(serializers.ModelSerializer):
    departure_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%d %H:%M'])
    arrival_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%d %H:%M'])

    route = RouteSerializer(read_only=True)
    plane = PlaneSerializer(read_only=True)
    crew = CrewAndMembersSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'route', 'departure_point', 'arrival_point',
            'plane', 'crew', 'departure_datetime', 'arrival_datetime', 'sold_tickets', 'is_transit'
        ]

class FlightWithPlaneSerializer(serializers.ModelSerializer):
    plane = PlaneSerializer(read_only=True)
    route = serializers.SerializerMethodField()

    departure_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=["%Y-%m-%d %H:%M"])
    arrival_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=["%Y-%m-%d %H:%M"])

    def get_route(self, obj):
        return {
            "id": obj.route.id,
            "departure_point": obj.route.departure_point,
            "destination_point": obj.route.destination_point
        }

    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'route', 'departure_point', 'arrival_point',
            'departure_datetime', 'arrival_datetime', 'sold_tickets', 'plane', 'crew', 'is_transit'
        ]