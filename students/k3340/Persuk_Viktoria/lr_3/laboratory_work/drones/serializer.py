from rest_framework import serializers
from .models import Drones, Flights, FlightLogs, Documents


class FlightLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightLogs
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']


class FlightSerializer(serializers.ModelSerializer):
    logs = FlightLogSerializer(many=True, read_only=True)

    class Meta:
        model = Flights
        fields = '__all__'
        read_only_fields = ['id']


class DocumentSerializer(serializers.ModelSerializer):
    # drone_id необязательный при создании через вложенный URL /drones/{id}/documents/
    drone_id = serializers.PrimaryKeyRelatedField(
        queryset=Drones.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Documents
        fields = '__all__'
        read_only_fields = ['id', 'uploaded_at']


class DroneSerializer(serializers.ModelSerializer):
    flights = FlightSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Drones
        fields = '__all__'
