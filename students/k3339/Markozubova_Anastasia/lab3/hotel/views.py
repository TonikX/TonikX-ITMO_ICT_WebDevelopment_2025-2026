from rest_framework import viewsets
from .models import Floor, Room, Client, StayRecord, Employee, CleaningSchedule, CleaningRecord
from .serializers import (
    FloorSerializer, RoomSerializer, ClientSerializer,
    StayRecordSerializer, EmployeeSerializer,
    CleaningScheduleSerializer, CleaningRecordSerializer, FloorDetailSerializer
)
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response


class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FloorDetailSerializer
        return FloorSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    def usage_stats(self, request):
        rooms = Room.objects.annotate(
            stays_count=Count('stay_records')
        ).values(
            'id', 'number', 'room_type', 'price_per_day', 'stays_count'
        )
        return Response(rooms)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False, methods=['get'])
    def activity_stats(self, request):
        clients = Client.objects.annotate(
            stays_count=Count('stay_records')
        ).values(
            'id', 'first_name', 'last_name', 'city', 'stays_count'
        ).order_by('-stays_count')

        return Response(clients)



class StayRecordViewSet(viewsets.ModelViewSet):
    queryset = StayRecord.objects.all()
    serializer_class = StayRecordSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer


class CleaningRecordViewSet(viewsets.ModelViewSet):
    queryset = CleaningRecord.objects.all()
    serializer_class = CleaningRecordSerializer
