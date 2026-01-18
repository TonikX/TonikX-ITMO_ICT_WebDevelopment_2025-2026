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

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')

        if start and end and start >= end:
            raise serializers.ValidationError("дата заезда должна быть раньше даты выезда")

        return data


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