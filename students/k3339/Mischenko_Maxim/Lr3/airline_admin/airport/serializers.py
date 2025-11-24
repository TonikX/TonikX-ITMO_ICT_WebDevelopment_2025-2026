from rest_framework import serializers
from .models import (
    Company, PlaneType, Aircraft,
    Airport, Flight, Stopover,
    CrewMember, Crew, CrewAssignment,
    CrewMemberFlightPermission
)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class PlaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaneType
        fields = "__all__"

class AircraftSerializer(serializers.ModelSerializer):
    plane_type = PlaneTypeSerializer(read_only=True)
    plane_type_id = serializers.PrimaryKeyRelatedField(
        queryset=PlaneType.objects.all(), source="plane_type", write_only=True
    )
    owner_company = CompanySerializer(read_only=True)
    owner_company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source="owner_company", write_only=True
    )

    class Meta:
        model = Aircraft
        fields = [
            "id", "registration_number", "plane_type", "plane_type_id",
            "seats", "cruise_speed_kmh", "owner_company", "owner_company_id"
        ]

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"

class StopoverSerializer(serializers.ModelSerializer):
    airport = AirportSerializer(read_only=True)
    airport_id = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all(), source="airport", write_only=True)

    class Meta:
        model = Stopover
        fields = ["id", "flight", "order", "airport", "airport_id", "arrival_datetime", "departure_datetime"]
        read_only_fields = ["flight"]

class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = "__all__"

class CrewAssignmentSerializer(serializers.ModelSerializer):
    member = CrewMemberSerializer(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(queryset=CrewMember.objects.all(), source="member", write_only=True)

    class Meta:
        model = CrewAssignment
        fields = ["id", "crew", "member", "member_id", "role", "is_active"]

class CrewSerializer(serializers.ModelSerializer):
    members = CrewMemberSerializer(many=True, read_only=True)
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = Crew
        fields = ["id", "name", "members", "assignments"]

    def get_assignments(self, obj):
        qs = obj.crewassignment_set.all()
        return CrewAssignmentSerializer(qs, many=True).data

class FlightSerializer(serializers.ModelSerializer):
    aircraft = AircraftSerializer(read_only=True)
    aircraft_id = serializers.PrimaryKeyRelatedField(queryset=Aircraft.objects.all(), source="aircraft", write_only=True, allow_null=True, required=False)
    departure_airport = AirportSerializer(read_only=True)
    departure_airport_id = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all(), source="departure_airport", write_only=True)
    arrival_airport = AirportSerializer(read_only=True)
    arrival_airport_id = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all(), source="arrival_airport", write_only=True)
    crew = CrewSerializer(read_only=True)
    crew_id = serializers.PrimaryKeyRelatedField(queryset=Crew.objects.all(), source="crew", write_only=True, allow_null=True, required=False)
    stopovers = StopoverSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = [
            "id", "flight_number", "aircraft", "aircraft_id",
            "distance_km", "departure_airport", "departure_airport_id",
            "arrival_airport", "arrival_airport_id",
            "departure_datetime", "arrival_datetime",
            "crew", "crew_id", "sold_tickets", "stopovers",
        ]

class CrewMemberFlightPermissionSerializer(serializers.ModelSerializer):
    member = CrewMemberSerializer(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(queryset=CrewMember.objects.all(), source="member", write_only=True)
    flight = FlightSerializer(read_only=True)
    flight_id = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all(), source="flight", write_only=True)

    class Meta:
        model = CrewMemberFlightPermission
        fields = ["id", "flight", "flight_id", "member", "member_id", "allowed", "issued_by", "issued_at", "comment"]
        read_only_fields = ["issued_by", "issued_at"]
