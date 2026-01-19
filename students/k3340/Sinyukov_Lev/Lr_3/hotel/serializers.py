from rest_framework import serializers
from .models import Room, Client, Stay, Employee, CleaningSchedule


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class CleaningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = "__all__"


class StayShortSerializer(serializers.ModelSerializer):
    room_number = serializers.IntegerField(source="room.number", read_only=True)

    class Meta:
        model = Stay
        fields = ["id", "check_in", "check_out", "room_number"]


class ClientDetailSerializer(serializers.ModelSerializer):
    stays = StayShortSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = "__all__"


class ClientShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "passport_number", "last_name", "first_name"]


class RoomDetailSerializer(serializers.ModelSerializer):
    stays = serializers.SerializerMethodField()

    def get_stays(self, obj):
        stays = obj.stays.select_related("client")
        return [
            {
                "id": s.id,
                "check_in": s.check_in,
                "check_out": s.check_out,
                "client": ClientShortSerializer(s.client).data,
            }
            for s in stays
        ]

    class Meta:
        model = Room
        fields = "__all__"