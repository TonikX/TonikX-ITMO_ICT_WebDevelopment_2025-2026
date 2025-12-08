from rest_framework import generics
from .models import (
    Airport,
    Company,
    PlaneType,
    Plane,
    Route,
    Flight,
    FlightInstance,
    TransitStop,
    Passenger,
    Seat,
    Ticket,
    CrewMember,
    Crew,
)
from .serializers import (
    AirportSerializer,
    CompanySerializer,
    PlaneTypeSerializer,
    PlaneSerializer,
    RouteSerializer,
    FlightSerializer,
    FlightInstanceSerializer,
    TransitStopSerializer,
    PassengerSerializer,
    SeatSerializer,
    TicketSerializer,
    CrewMemberSerializer,
    CrewSerializer,
    RouteWithFlightsSerializer,
    FlightInstanceWithCrewSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper


# ====== AIRPORT ======

class AirportListCreateView(generics.ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


# ====== COMPANY ======

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


# ====== PLANE TYPE ======

class PlaneTypeListCreateView(generics.ListCreateAPIView):
    queryset = PlaneType.objects.all()
    serializer_class = PlaneTypeSerializer


class PlaneTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlaneType.objects.all()
    serializer_class = PlaneTypeSerializer


# ====== PLANE ======

class PlaneListCreateView(generics.ListCreateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer


class PlaneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer


# ====== ROUTE ======

class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


# ====== FLIGHT ======

class FlightListCreateView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


# ====== FLIGHT INSTANCE ======

class FlightInstanceListCreateView(generics.ListCreateAPIView):
    queryset = FlightInstance.objects.all()
    serializer_class = FlightInstanceSerializer


class FlightInstanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FlightInstance.objects.all()
    serializer_class = FlightInstanceSerializer


# ====== TRANSIT STOP ======

class TransitStopListCreateView(generics.ListCreateAPIView):
    queryset = TransitStop.objects.all()
    serializer_class = TransitStopSerializer


class TransitStopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransitStop.objects.all()
    serializer_class = TransitStopSerializer


# ====== PASSENGER ======

class PassengerListCreateView(generics.ListCreateAPIView):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer


class PassengerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer


# ====== SEAT ======

class SeatListCreateView(generics.ListCreateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class SeatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


# ====== TICKET ======

class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


# ====== CREW MEMBER ======

class CrewMemberListCreateView(generics.ListCreateAPIView):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer


class CrewMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer


# ====== CREW (назначение на рейс) ======

class CrewListCreateView(generics.ListCreateAPIView):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class CrewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


# ВЛОЖЕННЫЙ GET: ОДИН-КО-МНОГИМ (Route -> Flight)

class RouteWithFlightsView(generics.RetrieveAPIView):
    """
    Возвращает один маршрут и список всех рейсов по этому маршруту.
    Пример: GET /api/routes/1/with-flights/
    """
    queryset = Route.objects.all()
    serializer_class = RouteWithFlightsSerializer



# ВЛОЖЕННЫЙ GET: МНОГИЕ-КО-МНОГИМ (FlightInstance <-> CrewMember)

class FlightInstanceWithCrewView(generics.RetrieveAPIView):
    """
    Возвращает конкретный вылет и список членов экипажа, которые на нём работают.
    Пример: GET /api/flight-instances/1/with-crew/
    """
    queryset = FlightInstance.objects.all()
    serializer_class = FlightInstanceWithCrewSerializer






#  АНАЛИТИКА 1: Марка самолёта, которая чаще всего летает по маршруту
# GET /api/routes/<int:pk>/top-plane-type/
class RouteTopPlaneTypeView(APIView):
    """
    Для заданного маршрута возвращает тип самолёта, который чаще всего выполнял рейсы.
    """
    def get(self, request, pk):
        route_id = pk

        plane_type = (
            PlaneType.objects
            .filter(planes__flight_instances__flight__route_id=route_id)
            .annotate(flights_count=Count("planes__flight_instances", distinct=True))
            .order_by("-flights_count")
            .first()
        )

        if not plane_type:
            return Response(
                {"detail": "Для этого маршрута ещё нет выполненных рейсов."},
                status=404,
            )

        data = {
            "route_id": route_id,
            "plane_type_id": plane_type.id,
            "plane_type_name": plane_type.name,
            "seat_count": plane_type.seat_count,
            "cruise_speed": plane_type.cruise_speed,
            "flights_count": plane_type.flights_count,
        }
        return Response(data)




# АНАЛИТИКА 2: Маршруты с недозаполненными рейсами
# GET /api/analytics/underfilled-routes/?percent=70
class UnderfilledRoutesView(APIView):
    """
    Ищет рейсы, у которых процент занятости мест меньше заданного,
    и возвращает список таких рейсов с информацией о маршруте.
    """
    def get(self, request):
        try:
            percent = float(request.query_params.get("percent", 70))
        except ValueError:
            percent = 70.0

        # Для каждого конкретного вылета считаем количество мест и проданных билетов
        qs = (
            FlightInstance.objects
            .annotate(
                seats_count=Count("seats", distinct=True),
                sold_count=Count(
                    "tickets",
                    filter=Q(tickets__status__in=["booked", "paid"]),
                    distinct=True,
                ),
            )
            .exclude(seats_count=0)
        )

        # выражение sold_count * 100 / seats_count
        occupancy_expr = ExpressionWrapper(
            F("sold_count") * 100.0 / F("seats_count"),
            output_field=FloatField(),
        )

        qs = qs.annotate(occupancy_percent=occupancy_expr).filter(
            occupancy_percent__lt=percent
        )

        result = []
        for fi in qs.select_related("flight__route"):
            route = fi.flight.route
            result.append({
                "flight_instance_id": fi.id,
                "flight_number": fi.flight.flight_number,
                "route_id": route.id,
                "route": f"{route.departure_airport.airport_code} -> {route.destination_airport.airport_code}",
                "occupancy_percent": round(fi.occupancy_percent, 2),
            })

        return Response({
            "limit_percent": percent,
            "items": result,
        })



#  АНАЛИТИКА 3: Свободные места на конкретный вылет
# GET /api/flight-instances/<int:pk>/free-seats/
class FlightInstanceFreeSeatsView(APIView):
    """
    Возвращает список свободных мест для конкретного вылета.
    Свободное место = не забронировано и без билета.
    """
    def get(self, request, pk):
        seats = Seat.objects.filter(
            flight_instance_id=pk,
            is_booked=False,
            ticket__isnull=True,
        ).order_by("seat_number")

        serializer = SeatSerializer(seats, many=True)
        return Response({
            "flight_instance_id": pk,
            "free_seats_count": seats.count(),
            "seats": serializer.data,
        })



#  АНАЛИТИКА 4: Количество самолётов в ремонте
# GET /api/analytics/planes-in-maintenance/
class PlanesInMaintenanceView(APIView):
    """
    Возвращает количество самолётов со статусом 'maintenance'.
    """
    def get(self, request):
        count = Plane.objects.filter(status="maintenance").count()
        return Response({"planes_in_maintenance": count})



#  АНАЛИТИКА 5: Количество работников авиакомпании
# GET /api/companies/<int:pk>/employees-count/
class CompanyEmployeesCountView(APIView):
    """
    Возвращает количество активных сотрудников компании.
    """
    def get(self, request, pk):
        company_id = pk
        total = CrewMember.objects.filter(
            company_id=company_id,
            is_active=True,
        ).count()
        return Response({
            "company_id": company_id,
            "active_employees": total,
        })


#  АНАЛИТИКА 6: Отчёт по бортам компании по маркам
# GET /api/companies/<int:pk>/planes-report/
class CompanyPlanesReportView(APIView):
    """
    Отчёт о самолётах компании:
    - общее количество бортов
    - количество по каждой марке (PlaneType) + характеристики марки.
    """
    def get(self, request, pk):
        company_id = pk

        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response({"detail": "Компания не найдена."}, status=404)

        planes_qs = Plane.objects.filter(company_id=company_id)

        total_planes = planes_qs.count()

        type_stats = (
            PlaneType.objects
            .filter(planes__in=planes_qs)
            .annotate(planes_count=Count("planes"))
            .distinct()
        )

        types_data = []
        for pt in type_stats:
            types_data.append({
                "plane_type_id": pt.id,
                "plane_type_name": pt.name,
                "seat_count": pt.seat_count,
                "cruise_speed": pt.cruise_speed,
                "planes_count": pt.planes_count,
            })

        return Response({
            "company_id": company.id,
            "company_name": company.name,
            "total_planes": total_planes,
            "by_plane_type": types_data,
        })
