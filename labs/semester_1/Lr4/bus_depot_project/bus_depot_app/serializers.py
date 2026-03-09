from rest_framework import serializers
from .models import (
    BusType,
    Bus,
    Route,
    Driver,
    DriverAssignment,
    BusStatus,
)


# ==== Базовые сериализаторы =====


class BusTypeSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для типа автобуса.
    """
    class Meta:
        model = BusType
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для автобуса.
    """
    class Meta:
        model = Bus
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для маршрута.
    """
    class Meta:
        model = Route
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для водителя.
    """
    class Meta:
        model = Driver
        fields = '__all__'


class DriverAssignmentSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для назначения водителя.
    """
    class Meta:
        model = DriverAssignment
        fields = '__all__'


class BusStatusSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для статуса автобуса.
    """
    class Meta:
        model = BusStatus
        fields = '__all__'


# ===== Сериализаторы для специальных запросов =====


class DriverWithAssignmentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для водителя с его назначениями.
    """
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = '__all__'
    
    def get_assignments(self, obj):
        assignments = DriverAssignment.objects.filter(driver=obj)
        return DriverAssignmentSerializer(assignments, many=True).data


class RouteDriversSerializer(serializers.Serializer):
    """
    Сериализатор для маршрута с водителями и их графиком работы.
    """
    route = RouteSerializer()
    drivers = DriverWithAssignmentsSerializer(many=True)


class TotalRouteLengthSerializer(serializers.Serializer):
    """
    Сериализатор для общей протяжённости маршрутов.
    """
    total_length = serializers.IntegerField()
    routes_count = serializers.IntegerField()
    average_length = serializers.FloatField()


class BusStatusDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для статуса автобуса с детальной информацией об автобусе.
    """
    bus = BusSerializer(read_only=True)
    class Meta:
        model = BusStatus
        fields = '__all__'


class DriverClassStatsSerializer(serializers.Serializer):
    """
    Сериализатор для статистики по классам водителей.
    """
    driver_class = serializers.CharField()
    driver_class_display = serializers.CharField()
    count = serializers.IntegerField()


# ===== Сериализаторы для отчёта по автобусному парку =====


class ReportDriverSerializer(serializers.ModelSerializer):
    """
    Сериализатор для водителей для отчёта.
    """
    class Meta:
        model = Driver
        fields = [
            'id', 'full_name', 'passport', 'birth_date',
            'driver_class', 'experience', 'salary'
        ]


class ReportBusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для автобусов для отчёта.
    """
    drivers = ReportDriverSerializer(many=True)
    class Meta:
        model = Bus
        fields = [
            'id', 'license_plate', 'is_active', 'purchase_date',
            'drivers'
        ]


class ReportBusTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для типов автобуса для отчёта.
    """
    buses = ReportBusSerializer(many=True)
    class Meta:
        model = BusType
        fields = [
            'id', 'name', 'capacity',
            'buses'
        ]


class ReportRouterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для маршрутов для отчёта.
    """
    bus_types = ReportBusTypeSerializer(many=True)
    class Meta:
        model = Route
        fields = [
            'id', 'number', 'start_point', 'end_point',
            'start_time', 'end_time', 'interval', 'duration',
            'bus_types'
        ]


class ReportSummarySerializer(serializers.Serializer):
    """
    Сериализатор для общей статистики для отчёта.
    """
    total_routes = serializers.IntegerField()
    total_route_length_minutes = serializers.IntegerField()
    total_bus_types = serializers.IntegerField()
    bus_type_distribution = serializers.DictField()
    total_buses = serializers.IntegerField()
    total_drivers = serializers.IntegerField()
    drivers_average_experience = serializers.FloatField()
    drivers_class_distribution = serializers.DictField()


class ReportSerializer(serializers.Serializer):
    """
    Главный сериализатор для полного отчёта.
    """
    summary = ReportSummarySerializer()
    routes = ReportRouterSerializer(many=True)
