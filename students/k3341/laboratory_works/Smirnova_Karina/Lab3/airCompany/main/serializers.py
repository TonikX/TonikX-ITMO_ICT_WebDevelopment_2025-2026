from datetime import datetime

from rest_framework import serializers
from .models import AirlineCompany, Plane, Crew, CrewMember, Route, Flight, TransitLanding

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
    class Meta:
        model = CrewMember
        fields = '__all__'

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
    departure_datetime = serializers.DateTimeField(format=None, input_formats=None)
    arrival_datetime = serializers.DateTimeField(format=None, input_formats=None)

    class Meta:
        model = Flight
        fields = '__all__'

class TransitLandingSerializer(serializers.ModelSerializer):
    """
    Простой сериализатор для модели TransitLanding.
    """
    landing_datetime = serializers.DateTimeField(format=None, input_formats=None)
    takeoff_datetime = serializers.DateTimeField(format=None, input_formats=None)

    class Meta:
        model = TransitLanding
        fields = '__all__'

# Сериализаторы со связями

class CrewAndMembersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Crew + вложенные члены экипажа.
    """
    members = CrewMemberSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CrewMember.objects.all(), write_only=True, source='members', required=False
    )

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
        fields = ['id', 'flight_number', 'departure_datetime', 'arrival_datetime', 'plane']

class RouteWithFlightsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Route + вложенные рейсы.
    """
    flights = FlightInRouteSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = [
            'id', 'departure_point', 'destination_point',
            'distance', 'landing_points', 'transit_landings',
            'flights'
        ]

class AirlineCompanyAndPlanesAndCrewMembersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для AirlineCompany + вложенные самолеты и члены экипажа.
    """
    # one-to-many: company -> planes
    planes = PlaneSerializer(many=True, read_only=True, source='plane_set')
    # many-to-many: company -> crew members (обратная сторона CrewMember.company)
    crew_members = CrewMemberSerializer(many=True, read_only=True)

    class Meta:
        model = AirlineCompany
        fields = ['id', 'name', 'planes', 'crew_members']

class FlightWithTransitLandingsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Flight + вложенные transit landings.
    """
    transitlandings = TransitLandingSerializer(many=True, read_only=True, source='transitlanding_set')

    class Meta:
        model = Flight

        fields = [
            'id', 'flight_number', 'route', 'route_id',
            'departure_datetime', 'arrival_datetime', 'sold_tickets',
            'transitlandings'
        ]

class FlightInPlaneSerializer(serializers.ModelSerializer):
    """
    Небольшой сериализатор для рейса внутри объекта Самолёта.
    """
    departure_datetime = serializers.DateTimeField(format=None, input_formats=None)
    arrival_datetime = serializers.DateTimeField(format=None, input_formats=None)
    route = RouteSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'route', 'departure_datetime', 'arrival_datetime', 'sold_tickets']

class PlaneWithFlightsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Самолёта с вложенным списком рейсов (flight_set).
    Использует source='flight_set' — обратная связь Flight -> Plane (без related_name).
    """
    flights = FlightInPlaneSerializer(many=True, read_only=True, source='flight_set')
    airline_company = AirlineCompanySerializer(read_only=True)

    class Meta:
        model = Plane
        fields = ['id', 'number', 'type', 'seats_capacity', 'flight_speed', 'in_repair', 'airline_company', 'flights']