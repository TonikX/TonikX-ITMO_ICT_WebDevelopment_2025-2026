from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import (
    Company, PlaneType, Aircraft,
    Airport, Flight, Stopover,
    CrewMember, Crew, CrewAssignment,
    CrewMemberFlightPermission
)
from .serializers import (
    CompanySerializer, PlaneTypeSerializer, AircraftSerializer,
    AirportSerializer, FlightSerializer, StopoverSerializer,
    CrewMemberSerializer, CrewSerializer, CrewAssignmentSerializer,
    CrewMemberFlightPermissionSerializer
)

User = get_user_model()

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class PlaneTypeViewSet(viewsets.ModelViewSet):
    queryset = PlaneType.objects.all()
    serializer_class = PlaneTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.select_related("plane_type", "owner_company").all()
    serializer_class = AircraftSerializer
    permission_classes = [permissions.IsAuthenticated]

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [permissions.IsAuthenticated]

class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.select_related("employer").all()
    serializer_class = CrewMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.prefetch_related("members").all()
    serializer_class = CrewSerializer
    permission_classes = [permissions.IsAuthenticated]

class CrewAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CrewAssignment.objects.select_related("crew", "member").all()
    serializer_class = CrewAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related("aircraft", "departure_airport", "arrival_airport", "crew").prefetch_related("stopovers").all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="set-sold-tickets")
    def set_sold_tickets(self, request, pk=None):
        flight = self.get_object()
        sold = int(request.data.get("sold_tickets", flight.sold_tickets))
        flight.sold_tickets = sold
        flight.save()
        return Response({"flight": flight.flight_number, "sold_tickets": flight.sold_tickets})

class StopoverViewSet(viewsets.ModelViewSet):
    queryset = Stopover.objects.select_related("flight", "airport").all()
    serializer_class = StopoverSerializer
    permission_classes = [permissions.IsAuthenticated]

class CrewMemberFlightPermissionViewSet(viewsets.ModelViewSet):
    queryset = CrewMemberFlightPermission.objects.select_related("flight", "member", "issued_by").all()
    serializer_class = CrewMemberFlightPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(issued_by=self.request.user)
