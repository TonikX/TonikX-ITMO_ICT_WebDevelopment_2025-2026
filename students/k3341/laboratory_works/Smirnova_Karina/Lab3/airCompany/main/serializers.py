from datetime import datetime

from rest_framework import serializers
from .models import AirlineCompany, Plane, Crew, CrewMember, Route, Flight, TransitLanding

class AirlineCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = AirlineCompany
        fields = '__all__'

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = '__all__'

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'

class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    departure_datetime = serializers.DateTimeField(format=None, input_formats=None)
    arrival_datetime = serializers.DateTimeField(format=None, input_formats=None)

    class Meta:
        model = Flight
        fields = '__all__'

class TransitLandingSerializer(serializers.ModelSerializer):
    landing_datetime = serializers.DateTimeField(format=None, input_formats=None)
    takeoff_datetime = serializers.DateTimeField(format=None, input_formats=None)

    class Meta:
        model = TransitLanding
        fields = '__all__'

class TransitLandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitLanding
        fields = '__all__'