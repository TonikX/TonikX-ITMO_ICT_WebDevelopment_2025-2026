from rest_framework import serializers
from .models import (
    Airport,
    Company,
    PlaneType,
    Plane,
    Route,
    Flight,
    FlightInstance,
    TransitStop,
    Passenger,
    Seat,
    Ticket,
    CrewMember,
    Crew,
)


# ====== БАЗОВЫЕ СУЩНОСТИ ======

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class PlaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaneType
        fields = "__all__"


class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class FlightInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightInstance
        fields = "__all__"


class TransitStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitStop
        fields = "__all__"


# ====== ПАССАЖИРЫ, МЕСТА, БИЛЕТЫ ======

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


# ====== ПЕРСОНАЛ ======

class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class RouteWithFlightsSerializer(serializers.ModelSerializer):
    flights = FlightSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = "__all__"


class FlightInstanceWithCrewSerializer(serializers.ModelSerializer):
    crew_members = CrewMemberSerializer(many=True, read_only=True)

    class Meta:
        model = FlightInstance
        fields = "__all__"
