from rest_framework import serializers
from .models import (
    DriverClass, Driver,
    BusType, Bus,
    Route, WorkShift, BusDepot
)

# Класс водителя
class DriverClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverClass
        fields = '__all__'

# Водители
class DriverSerializer(serializers.ModelSerializer):
    driver_class = DriverClassSerializer(read_only=True)
    driver_class_id = serializers.PrimaryKeyRelatedField(
        queryset=DriverClass.objects.all(),
        source='driver_class',
        write_only=True
    )
    salary = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Driver
        fields = (
            'id',
            'first_name',
            'last_name',
            'passport_number',
            'birth_date',
            'experience_years',
            'driver_class',
            'driver_class_id',
            'salary'
        )

# Типы автобусов
class BusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusType
        fields = '__all__'

class BusDepotSerializer(serializers.ModelSerializer):
    current_occupancy = serializers.IntegerField(read_only=True)
    free_spaces = serializers.IntegerField(read_only=True)

    class Meta:
        model = BusDepot
        fields = '__all__'
        read_only_fields = ['current_occupancy', 'free_spaces']

# Автобусы
class BusSerializer(serializers.ModelSerializer):
    bus_type = BusTypeSerializer(read_only=True)
    bus_type_id = serializers.PrimaryKeyRelatedField(
        queryset=BusType.objects.all(),
        source='bus_type',
        write_only=True
    )

    depot = BusDepotSerializer(read_only=True)
    depot_id = serializers.PrimaryKeyRelatedField(
        queryset=BusDepot.objects.all(),
        source='depot',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Bus
        fields = (
            'id',
            'registration_number',
            'is_active',
            'bus_type',
            'bus_type_id',
            'depot',
            'depot_id',
        )

# Маршрут
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'



# Рабочая сменя
class WorkShiftSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(read_only=True)
    bus = BusSerializer(read_only=True)
    route = RouteSerializer(read_only=True)

    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(),
        source='driver',
        write_only=True
    )
    bus_id = serializers.PrimaryKeyRelatedField(
        queryset=Bus.objects.all(),
        source='bus',
        write_only=True
    )
    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(),
        source='route',
        write_only=True
    )

    class Meta:
        model = WorkShift
        fields = (
            'id',
            'date',
            'start_time',
            'end_time',
            'absence_reason',
            'driver',
            'driver_id',
            'bus',
            'bus_id',
            'route',
            'route_id'
        )
