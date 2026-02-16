from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import *

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = "__all__"

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    room_type_details = RoomTypeSerializer(source='room_type', read_only=True)
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())

    floor_details = FloorSerializer(source='floor', read_only=True)
    floor = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all())
  
    class Meta:
        model = Room
        fields = "__all__"

class GuestSerializer(serializers.ModelSerializer):
    city_details = CitySerializer(source='city', read_only=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    class Meta:
        model = Guest
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    guest_details = GuestSerializer(source='guest', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)
    
    guest = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    is_active = serializers.BooleanField(default=True, initial=True)

    class Meta:
        model = Booking
        fields = "__all__"
    
    def validate(self, data):
        instance_data = {}
        if self.instance:
            instance_data = {
                'room': self.instance.room, 'guest': self.instance.guest,
                'check_in': self.instance.check_in, 'check_out': self.instance.check_out,
                'is_active': self.instance.is_active
            }
        instance_data.update(data)

        try:
            temp_instance = Booking(**instance_data)
        except TypeError:
            return data 

        if self.instance:
            temp_instance.pk = self.instance.pk
            
        try:
            temp_instance.clean()
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                raise serializers.ValidationError(e.message_dict)
            else:
                raise serializers.ValidationError(e.messages)
        return data

class CleaningScheduleSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_of_week_display', read_only=True)

    floor_details = FloorSerializer(source='floor', read_only=True)
    floor = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all())

    class Meta:
        model = CleaningSchedule
        fields = "__all__"
