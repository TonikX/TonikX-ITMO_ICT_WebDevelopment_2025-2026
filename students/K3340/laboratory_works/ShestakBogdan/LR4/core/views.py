from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from .models import Driver, BusType, Bus, Route, WorkShift
from .serializers import (
    DriverSerializer, BusTypeSerializer, BusSerializer,
    RouteSerializer, WorkShiftSerializer
)


class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        # сначала просто проверяем, что юзер авторизован
        if not super().has_permission(request, view):
            return False
        # чтение всем авторизованным
        if request.method in SAFE_METHODS:
            return True
        # изменения только админам
        return request.user.is_staff

class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['get'])
    def by_class(self, request):
        agg = self.get_queryset().values('driver_class').annotate(count=Count('id'))
        return Response(list(agg))


class BusTypeViewSet(ModelViewSet):
    queryset = BusType.objects.all()
    serializer_class = BusTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class BusViewSet(ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAdminOrReadOnly]


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['get'])
    def total_duration(self, request):
        total = self.get_queryset().aggregate(total=Sum('duration_minutes'))['total'] or 0
        return Response({'total_duration_minutes': total})


class WorkShiftViewSet(ModelViewSet):
    queryset = WorkShift.objects.select_related('driver', 'bus', 'route')
    serializer_class = WorkShiftSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Список водителей по маршруту + их смены
    @action(detail=False, methods=['get'])
    def drivers_by_route(self, request):
        route_id = request.query_params.get('route_id')
        qs = self.queryset.filter(route_id=route_id).select_related('driver')
        data = {}
        for shift in qs:
            d = shift.driver
            data.setdefault(d.id, {
                'driver': d.full_name,
                'class': d.driver_class,
                'shifts': []
            })
            data[d.id]['shifts'].append({
                'date': shift.date,
                'start_time': shift.start_time,
                'end_time': shift.end_time,
                'status': shift.status,
            })
        return Response(list(data.values()))

    # Автобусы, не вышедшие на линию в день
    @action(detail=False, methods=['get'])
    def not_on_line(self, request):
        date_str = request.query_params.get('date')
        qs = self.queryset.filter(date=date_str).exclude(status='ON_LINE')
        result = []
        for shift in qs:
            result.append({
                'date': shift.date,
                'bus': shift.bus.reg_number,
                'driver': shift.driver.full_name,
                'route': shift.route.number,
                'status': shift.status,
                'reason': shift.reason,
            })
        return Response(result)


# Отчёт по автопарку
from rest_framework.views import APIView

class ParkReportView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        result = []
        types = BusType.objects.all()
        today = date.today()

        for t in types:
            buses = t.buses.all()
            bus_ids = buses.values_list('id', flat=True)
            shifts = WorkShift.objects.filter(bus_id__in=bus_ids).select_related('route', 'driver')

            routes = {s.route.id: s.route for s in shifts}
            drivers = {s.driver.id: s.driver for s in shifts}

            total_route_duration = sum(r.duration_minutes for r in routes.values())

            ages = []
            exps = []
            for d in drivers.values():
                age = today.year - d.birth_date.year
                ages.append(age)
                exps.append(d.experience_years)

            avg_age = sum(ages) / len(ages) if ages else 0
            avg_exp = sum(exps) / len(exps) if exps else 0

            result.append({
                'bus_type': t.name,
                'capacity': t.capacity,
                'buses_count': buses.count(),
                'routes_count': len(routes),
                'total_routes_duration_minutes': total_route_duration,
                'drivers_count': len(drivers),
                'avg_driver_age': round(avg_age, 1),
                'avg_driver_experience_years': round(avg_exp, 1),
            })

        return Response(result)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'is_staff': request.user.is_staff,
    })