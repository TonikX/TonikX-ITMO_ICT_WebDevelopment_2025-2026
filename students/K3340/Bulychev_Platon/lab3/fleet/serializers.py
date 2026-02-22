from rest_framework import serializers
from .models import BusType, Bus, Route, Driver, Schedule, Absence


class BusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusType
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    bus_type_name = serializers.CharField(source='bus_type.name', read_only=True)
    class Meta:
        model = Bus
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    bus_reg = serializers.CharField(source='bus.reg_number', read_only=True)
    route_number = serializers.CharField(source='route.number', read_only=True)
    class Meta:
        model = Driver
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.__str__', read_only=True)
    bus_reg = serializers.CharField(source='bus.reg_number', read_only=True)
    route_number = serializers.CharField(source='route.number', read_only=True)
    class Meta:
        model = Schedule
        fields = '__all__'


class AbsenceSerializer(serializers.ModelSerializer):
    bus_reg = serializers.CharField(source='bus.reg_number', read_only=True)
    reason_display = serializers.CharField(source='get_reason_display', read_only=True)
    class Meta:
        model = Absence
        fields = '__all__'


class RouteReportSerializer(serializers.ModelSerializer):
    buses = BusSerializer(source='schedules.bus', many=False, read_only=True)
    drivers = DriverSerializer(source='drivers', many=True, read_only=True)
    class Meta:
        model = Route
        fields = '__all__'


class FleetReportSerializer(serializers.Serializer):
    bus_type = serializers.CharField()
    bus_count = serializers.IntegerField()
    routes = serializers.ListField()
    total_duration = serializers.IntegerField()
    driver_count = serializers.IntegerField()
    avg_age = serializers.FloatField(allow_null=True)
    avg_experience = serializers.FloatField(allow_null=True)
