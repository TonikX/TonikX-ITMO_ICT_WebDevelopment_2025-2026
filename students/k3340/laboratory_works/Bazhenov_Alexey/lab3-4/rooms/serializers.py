from rest_framework import serializers

from stays.models import Stay
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    occupied_places = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id',
            'number',
            'floor',
            'room_type',
            'capacity',
            'daily_rate',
            'phone_number',
            'is_active',
            'occupied_places',
        ]

    def get_occupied_places(self, obj: Room) -> int:
        return obj.stays.filter(status=Stay.Status.ACTIVE).count()


class RoomStaySerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()

    class Meta:
        model = Stay
        fields = ['id', 'client', 'check_in', 'check_out', 'status', 'total_cost']

    def get_client(self, obj: Stay) -> dict:
        client = obj.client
        return {
            'id': client.id,
            'full_name': client.full_name,
            'city': client.city,
        }

