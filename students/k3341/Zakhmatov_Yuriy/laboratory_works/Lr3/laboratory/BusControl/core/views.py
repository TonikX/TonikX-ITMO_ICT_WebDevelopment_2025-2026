from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.db.models import Count, Sum, Avg

from .models import DriverClass, Driver, BusType, Bus, Route, WorkShift, BusDepot
from .serializers import (
    DriverClassSerializer, DriverSerializer,
    BusTypeSerializer, BusSerializer,
    RouteSerializer, WorkShiftSerializer, BusDepotSerializer
)


class BusDepotViewSet(ModelViewSet):
    queryset = BusDepot.objects.all()
    serializer_class = BusDepotSerializer

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Статистика по автопарку"""
        depot = self.get_object()

        stats = {
            'depot': depot.name,
            'capacity': depot.capacity,
            'current_occupancy': depot.current_occupancy,
            'free_spaces': depot.free_spaces,
            'active_buses': depot.buses.filter(is_active=True).count(),
            'inactive_buses': depot.buses.filter(is_active=False).count(),
        }

        return Response(stats)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Сводная информация по всем автопаркам"""
        depots = BusDepot.objects.all()
        summary_data = []

        for depot in depots:
            summary_data.append({
                'id': depot.id,
                'name': depot.name,
                'address': depot.address,
                'capacity': depot.capacity,
                'occupancy': depot.current_occupancy,
                'occupancy_percentage': (
                    (depot.current_occupancy / depot.capacity * 100)
                    if depot.capacity > 0 else 0
                ),
                'active_buses': depot.buses.filter(is_active=True).count(),
            })

        return Response(summary_data)


# Классы водителей
class DriverClassViewSet(ModelViewSet):
    queryset = DriverClass.objects.all()
    serializer_class = DriverClassSerializer

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Количество водителей по классам
        """
        stats = Driver.objects.values('driver_class__name').annotate(total=Count('id'))
        return Response(stats)

# Водители
class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.select_related('driver_class')
    serializer_class = DriverSerializer

# Типы автобусов
class BusTypeViewSet(ModelViewSet):
    queryset = BusType.objects.all()
    serializer_class = BusTypeSerializer

    @action(detail=False, methods=['get'])
    def report(self, request):
        """
        Отчет по автопарку, сгруппированный по типам автобусов
        """
        report = []

        for bus_type in BusType.objects.all():
            buses = Bus.objects.filter(bus_type=bus_type)
            routes = Route.objects.filter(workshift__bus__in=buses).distinct()
            drivers = Driver.objects.filter(workshift__bus__in=buses).distinct()

            report.append({
                "bus_type": bus_type.name,
                "bus_count": buses.count(),
                "routes": RouteSerializer(routes, many=True).data,
                "drivers": DriverSerializer(drivers, many=True).data,
                "total_route_duration": routes.aggregate(total=Sum('duration_minutes'))['total'],
                "drivers_avg_experience": drivers.aggregate(avg=Avg('experience_years'))['avg'],
            })

        return Response(report)
# Автобусы
class BusViewSet(ModelViewSet):
    queryset = Bus.objects.select_related('bus_type')
    serializer_class = BusSerializer

# Маршруты
class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    @action(detail=True, methods=['get'])
    def drivers_schedule(self, request, pk=None):
        """
        Список водителей на маршруте с графиком работы
        """
        shifts = WorkShift.objects.filter(route_id=pk).select_related('driver')
        return Response([
            {
                "driver": f"{s.driver.last_name} {s.driver.first_name}",
                "date": s.date,
                "start_time": s.start_time,
                "end_time": s.end_time
            } for s in shifts
        ])

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """
        Время начала и окончания конкретного маршрута
        """
        try:
            route = Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            return Response({"error": "Маршрут не найден"}, status=404)

        return Response({
            "route": route.number,
            "start_time": route.start_time,
            "end_time": route.end_time
        })

    @action(detail=False, methods=['get'])
    def total_duration(self, request):
        """
        Общая протяженность всех маршрутов
        """
        total = Route.objects.aggregate(total_minutes=Sum('duration_minutes'))['total_minutes']
        return Response({"total_duration_minutes": total})

# График работы водителей (смены)
class WorkShiftViewSet(ModelViewSet):
    queryset = WorkShift.objects.select_related('driver', 'bus', 'route')
    serializer_class = WorkShiftSerializer

    @action(detail=False, methods=['get'])
    def missed(self, request):
        """
        Автобусы, не вышедшие на линию в заданный день
        """
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Укажите date=YYYY-MM-DD"}, status=400)

        date = parse_date(date_str)
        shifts = WorkShift.objects.filter(date=date, absence_reason__isnull=False).select_related('bus')
        return Response([
            {"bus": s.bus.registration_number, "reason": s.absence_reason} for s in shifts
        ])
