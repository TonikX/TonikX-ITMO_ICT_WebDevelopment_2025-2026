from django.utils import timezone
from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import Room, Client, Employee, CleaningSchedule
from django.db.models import Q
from datetime import date


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    @action(detail=False, methods=['get'])
    def room_history(self, request):
        room_number = request.query_params.get('room_number')
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        if not all([room_number, start_date, end_date]):
            return Response({'error': 'room_number, start, and end are required'}, status=400)

        room = get_object_or_404(Room, number=room_number)
        clients = room.clients.filter(
            check_in_date__lte=end_date,
            check_out_date__gte=start_date
        )
        return Response({
            'room': RoomSerializer(room).data,
            'clients': ClientSerializer(clients, many=True).data
        })

    @action(detail=False, methods=['get'])
    def free_rooms(self, request):
        start_date_str = request.query_params.get('start')
        end_date_str = request.query_params.get('end')
        if not start_date_str or not end_date_str:
            return Response({'error': 'start and end are required'}, status=400)
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        booked_room_ids = Client.objects.filter(
            room__isnull=False,
            check_in_date__lte=end_date,
            check_out_date__gte=start_date
        ).values_list('room_id', flat=True)
        free_rooms = Room.objects.exclude(id__in=booked_room_ids)
        serializer = RoomSerializer(free_rooms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def status(self, request):
        rooms = Room.objects.all()
        result = []
        for room in rooms:
            room_data = RoomSerializer(room).data
            today = timezone.now().date()
            occupied = Client.objects.filter(
                room=room,
                check_in_date__lte=today,
            ).filter(
                Q(check_out_date__gte=today) | Q(check_out_date__isnull=True)
            ).exists()
            room_data['free'] = not occupied
            result.append(room_data)
        return Response(result)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False, methods=['get'])
    def clients_town_count(self, request):
        town = request.query_params.get('town')
        if not town:
            return Response({'error': 'town parameter is required'}, status=400)

        clients_count = Client.objects.filter(city_of_origin=town).count()
        return Response({'clients_count': clients_count})

    @action(detail=True, methods=['get'])
    def same_clients(self, request, pk=None):
        client = get_object_or_404(Client, pk=pk)
        start_date = client.check_in_date
        end_date = client.check_out_date

        overlapping_clients = Client.objects.filter(
            check_in_date__lte=end_date,
            check_out_date__gte=start_date
        ).exclude(id=client.id)

        return Response({
            'client': ClientSerializer(client).data,
            'same_clients': ClientSerializer(overlapping_clients, many=True).data
        })
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        client = get_object_or_404(Client, pk=pk)

        client.check_out_date = timezone.now().date()
        client.room = None
        client.save()

        return Response({'status': 'client checked out'})


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer

    @action(detail=False, methods=['get'])
    def cleaning_schedule(self, request):
        client_id = request.query_params.get('client_id')
        day = request.query_params.get('day')

        if not all([client_id, day]):
            return Response({'error': 'client_id and day are required'}, status=400)

        client = get_object_or_404(Client, pk=client_id)
        cleaning_schedules = CleaningSchedule.objects.filter(
            floor=client.room.floor,
            day_of_week=day
        )

        serializer = CleaningScheduleWithEmployeeSerializer(cleaning_schedules, many=True)
        return Response({
            'client': ClientSerializer(client).data,
            'cleaning_schedule': serializer.data
        })