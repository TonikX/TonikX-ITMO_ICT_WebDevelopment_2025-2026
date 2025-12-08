from rest_framework import serializers
from .models import Driver, BusType, Bus, Route, WorkShift


class BusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusType
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    bus_type = BusTypeSerializer(read_only=True)
    bus_type_id = serializers.PrimaryKeyRelatedField(
        queryset=BusType.objects.all(),
        source='bus_type',
        write_only=True
    )

    class Meta:
        model = Bus
        fields = ['id', 'reg_number', 'bus_type', 'bus_type_id']


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    salary = serializers.ReadOnlyField()

    class Meta:
        model = Driver
        fields = '__all__'


class WorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShift
        fields = '__all__'