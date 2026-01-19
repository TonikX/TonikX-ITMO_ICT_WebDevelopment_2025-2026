from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Room, Client, Stay, Employee, CleaningSchedule
from .serializers import (
    RoomSerializer,
    ClientSerializer,
    StaySerializer,
    EmployeeSerializer,
    CleaningScheduleSerializer,
)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            from .serializers import RoomDetailSerializer
            return RoomDetailSerializer
        return RoomSerializer

    permission_classes = [IsAuthenticated]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            from .serializers import ClientDetailSerializer
            return ClientDetailSerializer
        return ClientSerializer

    permission_classes = [IsAuthenticated]


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer
    permission_classes = [IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    permission_classes = [IsAuthenticated]