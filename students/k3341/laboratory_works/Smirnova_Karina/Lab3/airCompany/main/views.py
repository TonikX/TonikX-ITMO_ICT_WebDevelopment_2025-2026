from django.db.models import Count, Avg
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AirlineCompany, Plane, Crew, Route, Flight, TransitLanding, CrewMember
from .serializers import AirlineCompanySerializer, PlaneSerializer, CrewSerializer, RouteSerializer, FlightSerializer, \
    TransitLandingSerializer, CrewMemberSerializer


class AirlineCompanyViewSet(viewsets.ModelViewSet):
    queryset = AirlineCompany.objects.all()
    serializer_class = AirlineCompanySerializer

class PlaneViewSet(viewsets.ModelViewSet):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class TransitLandingViewSet(viewsets.ModelViewSet):
    queryset = TransitLanding.objects.all()
    serializer_class = TransitLandingSerializer

class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer

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

class RoutesBelowCapacity(APIView):
    def get(self, request, percentage):
        try:
            # Рассчитываем порог заполненности
            threshold = float(percentage) / 100

            # Фильтруем маршруты с рейсами, заполненными менее чем на threshold
            under_capacity_routes = Route.objects.annotate(
                average_capacity=Avg('flights__sold_tickets') / Avg('flights__plane__seats_capacity')
            ).filter(average_capacity__lt=threshold)

            # Сериализуем данные маршрутов
            serializer = RouteSerializer(under_capacity_routes, many=True)

            return Response({'under_capacity_routes': serializer.data}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "Invalid percentage value."}, status=status.HTTP_400_BAD_REQUEST)

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