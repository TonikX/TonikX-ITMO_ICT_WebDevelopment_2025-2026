from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import RoomType, Room, Client, Staff, CleaningSchedule, Stay

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_hotel_staff', 'is_admin')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            is_hotel_staff=validated_data.get('is_hotel_staff', False),
            is_admin=validated_data.get('is_admin', False)
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_hotel_staff', 'is_admin')


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Staff
        fields = '__all__'


class CleaningScheduleSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.__str__', read_only=True)

    class Meta:
        model = CleaningSchedule
        fields = '__all__'


class StaySerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.__str__', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)

    class Meta:
        model = Stay
        fields = '__all__'