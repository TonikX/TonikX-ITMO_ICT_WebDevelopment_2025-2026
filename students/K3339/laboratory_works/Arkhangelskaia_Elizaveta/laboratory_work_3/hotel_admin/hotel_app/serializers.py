from rest_framework import serializers
from .models import *


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = "__all__"

class ResidentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residents
        fields = "__all__"


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workers
        fields = "__all__"

class RequestCleaningSerializer(serializers.Serializer):
    date = serializers.DateField(source='cleaning_day')
    room_number = serializers.CharField(source='room__room_number')
    worker_full_name = serializers.CharField()


class CleaningInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningInformation
        fields = "__all__"


class CleaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cleaning
        fields = "__all__"