from rest_framework import serializers
from .models import Floor, Room, Guest, LivingRecord, Staff, CleaningSchedule, CleaningRecord


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class LivingRecordSerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = LivingRecord
        fields = '__all__'

class LivingRecordSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LivingRecord
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class CleaningScheduleSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    floor = FloorSerializer(read_only=True)

    class Meta:
        model = CleaningSchedule
        fields = '__all__'

class CleaningScheduleSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = '__all__'

class FloorFullSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    cleaning_schedules = CleaningScheduleSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = '__all__'

class StaffFullSerializer(serializers.ModelSerializer):
    cleaning_schedules = CleaningScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Staff
        fields = '__all__'

class GuestFullSerializer(serializers.ModelSerializer):
    living_records = LivingRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Guest
        fields = '__all__'

class RoomFullSerializer(serializers.ModelSerializer):
    living_records = LivingRecordSerializer(many=True, read_only=True)
    floor = FloorFullSerializer(read_only=True)
    
    class Meta:
        model = Room
        fields = '__all__'

class CleaningRecordSerializer(serializers.ModelSerializer):
    floor = FloorSerializer(read_only=True)
    staff = StaffSerializer(read_only=True)

    class Meta:
        model = CleaningRecord
        fields = '__all__'

class CleaningRecordSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningRecord
        fields = '__all__'