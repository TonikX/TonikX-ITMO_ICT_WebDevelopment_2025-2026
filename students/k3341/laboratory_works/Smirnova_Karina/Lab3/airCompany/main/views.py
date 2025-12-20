from django.db.models import Count, Avg
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_protect

from .models import AirlineCompany, Plane, Crew, Route, Flight, CrewMember
from .serializers import (
    AirlineCompanySerializer,
    PlaneSerializer,
    CrewSerializer,
    RouteSerializer,
    FlightSerializer,
    CrewMemberSerializer,
    AirlineCompanyAndPlanesAndCrewMembersSerializer,
    PlaneWithFlightsSerializer,
    CrewAndMembersSerializer,
    RouteWithFlightsSerializer,
    FlightEverythingSerializer,
    PlaneWithCompanySerializer
)


class AirlineCompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели AirlineCompany с возможностью поиска по названию.
    """
    queryset = AirlineCompany.objects.all().prefetch_related('plane_set', 'crew_members')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AirlineCompanyAndPlanesAndCrewMembersSerializer
        elif self.action == 'create':
            return AirlineCompanySerializer
        return AirlineCompanyAndPlanesAndCrewMembersSerializer

class PlaneViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Plane + рейсы
    """
    queryset = Plane.objects.select_related('airline_company').prefetch_related('flight_set__route').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlaneWithFlightsSerializer
        elif self.action in ['create', 'update']:
            return PlaneSerializer
        return PlaneWithCompanySerializer

class CrewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Crew + члены экипажа
    """
    queryset = Crew.objects.prefetch_related('members').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'update', 'partial_update'):
            return CrewAndMembersSerializer
        return CrewSerializer

class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.prefetch_related('company').all()
    serializer_class = CrewMemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().prefetch_related('flights')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RouteWithFlightsSerializer
        return RouteSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related('route', 'plane').prefetch_related('crew__members').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return FlightEverythingSerializer
        if self.action in ('create', 'update'):
            return FlightSerializer
        return FlightSerializer

    def update(self, request, *args, **kwargs):
        print("Данные запроса:", request.data)  # Вывод для проверки формата данных
        return super().update(request, *args, **kwargs)

class MostPopularPlaneType(APIView):
    def get(self, request, route_id):
        # Фильтруем рейсы по маршруту
        flights = Flight.objects.filter(route_id=route_id)

        # Подсчитываем количество рейсов для каждой марки самолета
        plane_counts = flights.values('plane__type').annotate(count=Count('id')).order_by('-count')

        # Проверяем, есть ли данные
        if not plane_counts:
            return Response({"detail": "No flights found for the given route."}, status=status.HTTP_404_NOT_FOUND)

        # Получаем марку самолета с максимальным количеством рейсов
        most_popular_plane = plane_counts.first()

        return Response({
            "plane_type": most_popular_plane['plane__type'],
            "flight_count": most_popular_plane['count']
        }, status=status.HTTP_200_OK)

class RoutesBelowCapacity(APIView):
    def get(self, request, percentage):
        try:
            percentage_float = float(percentage)

            routes_with_capacity = []

            for route in Route.objects.all():
                flights = route.flights.select_related('plane').all()

                if not flights:
                    continue

                total_occupancy = 0
                valid_flights = 0

                for flight in flights:
                    if flight.plane and flight.plane.seats_capacity > 0:
                        occupancy = (flight.sold_tickets / flight.plane.seats_capacity) * 100
                        total_occupancy += occupancy
                        valid_flights += 1

                if valid_flights > 0:
                    avg_occupancy = total_occupancy / valid_flights

                    if avg_occupancy < percentage_float:
                        routes_with_capacity.append({
                            'id': route.id,
                            'route_id': route.id,
                            'departure_point': route.departure_point,
                            'destination_point': route.destination_point,
                            'distance': route.distance,
                            'landing_points': route.landing_points,
                            'transit_landings': route.transit_landings,
                            'average_occupancy': round(avg_occupancy, 2)
                        })

            return Response({'under_capacity_routes': routes_with_capacity}, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"detail": "Invalid percentage value."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AvailableSeats(APIView):
    def get(self, request, flight_id):
        try:
            # Получаем рейс по ID
            flight = Flight.objects.get(pk=flight_id)
        except Flight.DoesNotExist:
            return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)

        # Рассчитываем количество свободных мест
        available_seats = flight.plane.seats_capacity - flight.sold_tickets

        return Response({'available_seats': available_seats}, status=status.HTTP_200_OK)

class PlanesUnderRepair(APIView):
    def get(self, request):
        # Подсчитываем количество самолетов в ремонте
        under_repair_count = Plane.objects.filter(in_repair=True).count()

        return Response({'planes_under_repair': under_repair_count}, status=status.HTTP_200_OK)

class TotalEmployees(APIView):
    def get(self, request, company_id):
        try:
            # Получаем компанию-авиаперевозчика по ID
            company = AirlineCompany.objects.get(pk=company_id)
        except AirlineCompany.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

        # Подсчитываем количество работников компании
        total_employees = CrewMember.objects.filter(company=company).count()

        return Response({'total_employees': total_employees}, status=status.HTTP_200_OK)

class MostPopularPaneType(APIView):
    def get(self, request, route_id):
        # Фильтруем рейсы по маршруту
        flights = Flight.objects.filter(route_id=route_id)

        # Подсчитываем количество рейсов для каждой марки самолета
        plane_counts = flights.values('plane__type').annotate(count=Count('id')).order_by('-count')

        # Проверяем, есть ли данные
        if not plane_counts:
            return Response({"detail": "No flights found for the given route."}, status=status.HTTP_404_NOT_FOUND)

        # Получаем марку самолета с максимальным количеством рейсов
        most_popular_plane = plane_counts.first()

        return Response({
            "plane_type": most_popular_plane['plane__type'],
            "flight_count": most_popular_plane['count']
        }, status=status.HTTP_200_OK)

@csrf_protect
def auth_demo(request):
    """
    Обработчик страниц авторизации.
    """
    message = ''
    token = request.session.get('auth_token')
    user_info = None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'login':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Логиним пользователя в сессии
                django_login(request, user)
                # Создаём/получаем токен
                token_obj, created = Token.objects.get_or_create(user=user)
                request.session['auth_token'] = token_obj.key
                token = token_obj.key
                message = 'Успешный вход. Токен сохранён в сессии.'
            else:
                message = 'Неверный username или password.'
        elif action == 'me':
            if request.user.is_authenticated:
                u = request.user
                user_info = {
                    'id': u.id,
                    'username': u.username,
                    'email': u.email,
                    'is_active': u.is_active,
                    'is_staff': u.is_staff,
                }
            else:
                token_key = request.session.get('auth_token')
                if token_key:
                    try:
                        t = Token.objects.get(key=token_key)
                        u = t.user
                        user_info = {
                            'id': u.id,
                            'username': u.username,
                            'email': u.email,
                            'is_active': u.is_active,
                            'is_staff': u.is_staff,
                        }
                        message = 'Пользователь найден по токену из сессии.'
                    except Token.DoesNotExist:
                        message = 'Токен в сессии не найден.'
                else:
                    message = 'Нет активной сессии и токена. Сначала выполните вход.'
        elif action == 'logout':
            if request.user.is_authenticated:
                Token.objects.filter(user=request.user).delete()
                django_logout(request)
                request.session.pop('auth_token', None)
                message = 'Вышли из сессии и удалили токен.'
            else:
                token_key = request.session.pop('auth_token', None)
                if token_key:
                    Token.objects.filter(key=token_key).delete()
                    message = 'Токен из сессии удалён.'
                else:
                    message = 'Нет активной сессии и токена для удаления.'

    if user_info:
        import json
        user_info = json.dumps(user_info, ensure_ascii=False, indent=2)

    context = {
        'message': message,
        'token': token,
        'user_info': user_info,
    }
    return render(request, 'auth_page.html', context)