from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Avg, F, ExpressionWrapper, FloatField
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .permissions import IsStaffOrReadOnly
from datetime import datetime

# ViewSets для всех моделей с фильтрацией где нужно
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'code']


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.select_related('company').all()
    serializer_class = AircraftSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company', 'status', 'aircraft_type']
    search_fields = ['tail_number', 'aircraft_type']
    
    @action(detail=False, methods=['get'])
    def in_repair_count(self, request):
        """Запрос №4: Количество самолетов в ремонте"""
        in_repair_count = Aircraft.objects.filter(status='repair').count()
        return Response({'in_repair_count': in_repair_count})
    
    @action(detail=False, methods=['get'])
    def company_aircrafts_report(self, request):
        """Отчет о бортах компании"""
        company_id = request.query_params.get('company_id')
        
        if not company_id:
            return Response({'error': 'Параметр company_id обязателен'}, status=400)
        
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'error': 'Компания не найдена'}, status=404)
        
        aircrafts = Aircraft.objects.filter(company_id=company_id)
        total_count = aircrafts.count()
        
        if total_count == 0:
            return Response({
                'company_id': company_id,
                'company_name': company.name,
                'total_aircrafts': 0,
                'aircrafts_by_type': []
            })
        
        aircrafts_by_type = aircrafts.values('aircraft_type').annotate(
            count=Count('id'),
            avg_capacity=Avg('capacity'),
            avg_speed=Avg('speed'),
            active_count=Count('id', filter=Q(status='active')),
            repair_count=Count('id', filter=Q(status='repair'))
        ).order_by('-count')
        
        report_data = []
        for item in aircrafts_by_type:
            report_data.append({
                'aircraft_type': item['aircraft_type'],
                'count': item['count'],
                'percentage_of_total': round((item['count'] / total_count) * 100, 2),
                'avg_capacity': round(item['avg_capacity'], 2) if item['avg_capacity'] else 0,
                'avg_speed': round(item['avg_speed'], 2) if item['avg_speed'] else 0,
                'status_distribution': {
                    'active': item['active_count'],
                    'in_repair': item['repair_count']
                }
            })
        
        return Response({
            'company_id': company_id,
            'company_name': company.name,
            'total_aircrafts': total_count,
            'aircrafts_by_type': report_data
        })


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['code', 'name', 'city']


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('company').all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company', 'position', 'is_active']
    search_fields = ['first_name', 'last_name', 'passport']
    
    @action(detail=False, methods=['get'])
    def company_employees_count(self, request):
        """Запрос №5: Количество работников компании"""
        company_id = request.query_params.get('company_id')
        
        if not company_id:
            return Response({'error': 'Параметр company_id обязателен'}, status=400)
        
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'error': 'Компания не найдена'}, status=404)
        
        total_count = Employee.objects.filter(company_id=company_id).count()
        active_count = Employee.objects.filter(company_id=company_id, is_active=True).count()
        
        return Response({
            'company_id': company_id,
            'company_name': company.name,
            'total_employees': total_count,
            'active_employees': active_count,
            'inactive_employees': total_count - active_count
        })


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.select_related('company').all()
    serializer_class = CrewSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company', 'is_active']
    search_fields = ['name']


class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.select_related('crew', 'employee').all()
    serializer_class = CrewMemberSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['crew', 'employee', 'is_approved']


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        'departure_airport', 'arrival_airport', 'aircraft', 'crew'
    ).prefetch_related('transit_stops').all()
    
    serializer_class = FlightSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['departure_airport', 'arrival_airport', 'aircraft', 'crew']
    search_fields = ['flight_number']
    ordering_fields = ['departure_datetime', 'arrival_datetime', 'distance']
    ordering = ['-departure_datetime']
    
    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        """Запрос №3: Свободные места на рейс"""
        flight = self.get_object()
        
        available_seats = flight.aircraft.capacity - flight.tickets_sold
        load_percentage = (flight.tickets_sold / flight.aircraft.capacity * 100) if flight.aircraft.capacity > 0 else 0
        
        return Response({
            'flight_id': flight.id,
            'flight_number': flight.flight_number,
            'available_seats': available_seats,
            'load_percentage': round(load_percentage, 2),
            'has_available_seats': available_seats > 0
        })
    
    @action(detail=False, methods=['get'])
    def low_load_routes(self, request):
        """Запрос №2: Маршруты с рейсами заполненными менее чем на ХХ%"""
        try:
            threshold = float(request.query_params.get('threshold', 50))
        except ValueError:
            return Response({'error': 'Параметр threshold должен быть числом'}, status=400)
        
        if threshold < 0 or threshold > 100:
            return Response({'error': 'Параметр threshold должен быть в диапазоне 0-100'}, status=400)
        
        low_load_flights = Flight.objects.annotate(
            load_percentage=ExpressionWrapper(
                F('tickets_sold') * 100.0 / F('aircraft__capacity'),
                output_field=FloatField()
            )
        ).filter(
            load_percentage__lt=threshold,
            aircraft__capacity__gt=0
        ).select_related(
            'departure_airport', 'arrival_airport', 'aircraft'
        )
        
        routes_dict = {}
        for flight in low_load_flights:
            route_key = f"{flight.departure_airport.code}-{flight.arrival_airport.code}"
            
            if route_key not in routes_dict:
                routes_dict[route_key] = {
                    'departure': {
                        'code': flight.departure_airport.code,
                        'name': flight.departure_airport.name,
                        'city': flight.departure_airport.city
                    },
                    'arrival': {
                        'code': flight.arrival_airport.code,
                        'name': flight.arrival_airport.name,
                        'city': flight.arrival_airport.city
                    },
                    'flights': [],
                    'flights_count': 0,
                    'avg_load_percentage': 0
                }
            
            routes_dict[route_key]['flights'].append({
                'flight_number': flight.flight_number,
                'departure_datetime': flight.departure_datetime,
                'aircraft_type': flight.aircraft.aircraft_type,
                'tickets_sold': flight.tickets_sold,
                'capacity': flight.aircraft.capacity,
                'load_percentage': round(flight.load_percentage, 2)
            })
            routes_dict[route_key]['flights_count'] += 1
        
        routes_list = []
        for route_key, route_data in routes_dict.items():
            total_load = sum(f['load_percentage'] for f in route_data['flights'])
            route_data['avg_load_percentage'] = round(total_load / route_data['flights_count'], 2)
            routes_list.append(route_data)
        
        routes_list.sort(key=lambda x: x['avg_load_percentage'])
        
        return Response({
            'threshold': threshold,
            'routes_count': len(routes_list),
            'routes': routes_list
        })
    
    @action(detail=False, methods=['get'])
    def popular_aircraft_on_route(self, request):
        """Запрос №1: Марка самолета, которая чаще всего летает по маршруту"""
        departure_code = request.query_params.get('departure')
        arrival_code = request.query_params.get('arrival')
        
        if not departure_code or not arrival_code:
            return Response({
                'error': 'Необходимо указать параметры departure и arrival'
            }, status=400)
        
        try:
            departure_airport = Airport.objects.get(code=departure_code)
            arrival_airport = Airport.objects.get(code=arrival_code)
        except Airport.DoesNotExist:
            return Response({'error': 'Аэропорт не найден'}, status=404)
        
        flights = Flight.objects.filter(
            departure_airport=departure_airport,
            arrival_airport=arrival_airport
        ).select_related('aircraft')
        
        if not flights.exists():
            return Response({
                'error': f'Рейсы по маршруту {departure_code} -> {arrival_code} не найдены'
            }, status=404)
        
        aircraft_stats = {}
        for flight in flights:
            aircraft_type = flight.aircraft.aircraft_type
            if aircraft_type not in aircraft_stats:
                aircraft_stats[aircraft_type] = {'count': 0}
            aircraft_stats[aircraft_type]['count'] += 1
        
        most_popular_type = max(aircraft_stats.items(), key=lambda x: x[1]['count'])
        
        return Response({
            'route': f'{departure_code} -> {arrival_code}',
            'total_flights': flights.count(),
            'most_popular_aircraft': {
                'aircraft_type': most_popular_type[0],
                'flights_count': most_popular_type[1]['count'],
                'percentage': round((most_popular_type[1]['count'] / flights.count()) * 100, 2)
            }
        })


class TransitStopViewSet(viewsets.ModelViewSet):
    queryset = TransitStop.objects.select_related('flight', 'airport').all()
    serializer_class = TransitStopSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flight', 'airport']


# Пользовательские представления
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    user = request.user
    if request.method == 'PATCH':
        allowed = {'email', 'first_name', 'last_name'}
        data = {k: v for k, v in request.data.items() if k in allowed}
        for k, v in data.items():
            setattr(user, k, v)
        user.save(update_fields=list(data.keys()))
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser
    })
