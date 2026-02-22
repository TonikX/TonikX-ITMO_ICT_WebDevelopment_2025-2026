from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Sum, Avg
from django_filters.rest_framework import DjangoFilterBackend
from .models import BusType, Bus, Route, Driver, Schedule, Absence
from .serializers import (
    BusTypeSerializer, BusSerializer, RouteSerializer,
    DriverSerializer, ScheduleSerializer, AbsenceSerializer,
)


class BusTypeViewSet(viewsets.ModelViewSet):
    queryset = BusType.objects.all()
    serializer_class = BusTypeSerializer


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.select_related('bus_type').all()
    serializer_class = BusSerializer
    filterset_fields = ['bus_type']


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.select_related('bus', 'route').all()
    serializer_class = DriverSerializer
    filterset_fields = ['driver_class', 'route', 'bus']


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related('driver', 'bus', 'route').all()
    serializer_class = ScheduleSerializer
    filterset_fields = ['driver', 'route', 'date']


class AbsenceViewSet(viewsets.ModelViewSet):
    queryset = Absence.objects.select_related('bus').all()
    serializer_class = AbsenceSerializer
    filterset_fields = ['date', 'reason']


@api_view(['GET'])
def drivers_on_route(request, route_id):
    """drivers on a specific route with their schedules"""
    drivers = Driver.objects.filter(route_id=route_id).select_related('bus')
    data = []
    for d in drivers:
        schedules = Schedule.objects.filter(driver=d).order_by('date')
        data.append({
            'driver': DriverSerializer(d).data,
            'schedules': ScheduleSerializer(schedules, many=True).data,
        })
    return Response(data)


@api_view(['GET'])
def route_times(request):
    """start/end times for all routes"""
    routes = Route.objects.all().values('number', 'start_point', 'end_point', 'start_time', 'end_time')
    return Response(routes)


@api_view(['GET'])
def total_route_length(request):
    """total duration of all routes"""
    total = Route.objects.aggregate(total=Sum('duration_minutes'))
    return Response({'total_duration_minutes': total['total'] or 0})


@api_view(['GET'])
def absent_buses(request):
    """buses that didn't go on a given date with reason"""
    date = request.query_params.get('date')
    if not date:
        return Response({'error': 'date param required'}, status=status.HTTP_400_BAD_REQUEST)
    absences = Absence.objects.filter(date=date).select_related('bus')
    return Response(AbsenceSerializer(absences, many=True).data)


@api_view(['GET'])
def drivers_by_class(request):
    """count of drivers per class"""
    stats = Driver.objects.values('driver_class').annotate(count=Count('id')).order_by('driver_class')
    return Response(stats)


@api_view(['GET'])
def fleet_report(request):
    """report grouped by bus type with routes, drivers, stats"""
    bus_types = BusType.objects.all()
    report = []
    for bt in bus_types:
        buses = Bus.objects.filter(bus_type=bt)
        bus_ids = buses.values_list('id', flat=True)
        drivers = Driver.objects.filter(bus_id__in=bus_ids)
        routes = Route.objects.filter(drivers__bus__bus_type=bt).distinct()
        report.append({
            'bus_type': str(bt),
            'bus_count': buses.count(),
            'routes': [
                {
                    'route': RouteSerializer(r).data,
                    'buses': BusSerializer(Bus.objects.filter(bus_type=bt, schedules__route=r).distinct(), many=True).data,
                    'drivers': DriverSerializer(Driver.objects.filter(bus__bus_type=bt, route=r).distinct(), many=True).data,
                } for r in routes
            ],
            'total_duration': sum(r.duration_minutes for r in routes),
            'driver_count': drivers.count(),
            'avg_experience': drivers.aggregate(avg=Avg('experience_years'))['avg'],
        })
    return Response(report)
