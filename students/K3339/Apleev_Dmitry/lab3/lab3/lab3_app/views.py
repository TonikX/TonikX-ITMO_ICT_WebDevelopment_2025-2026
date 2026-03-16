from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.utils import timezone
from .models import Client, Room, Employee, CleaningSchedule
from .serializers import RoomSerializer, EmployeeSerializer, CleaningScheduleSerializer, ClientSerializer
from rest_framework.exceptions import ValidationError

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'room', 'passport_number']

    def is_room_available(self, room_id, check_in, check_out, exclude_id=None):
        overlapping = Client.objects.filter(
            room_id=room_id,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )

        if exclude_id:
            overlapping = overlapping.exclude(id=exclude_id)

        return not overlapping.exists()

    def perform_create(self, serializer):
        check_in = serializer.validated_data.get('check_in_date')
        check_out = serializer.validated_data.get('check_out_date')
        room = serializer.validated_data.get('room')

        if check_in >= check_out:
            raise ValidationError

        if not self.is_room_available(room.id, check_in, check_out):
            raise ValidationError
        serializer.save(booked_by=self.request.user if self.request.user.is_authenticated else None)


        check_in = serializer.validated_data.get('check_in_date', serializer.instance.check_in_date)
        check_out = serializer.validated_data.get('check_out_date', serializer.instance.check_out_date)
        room = serializer.validated_data.get('room', serializer.instance.room)

        if check_in >= check_out:
            raise ValidationError('Дата выезда должна быть позже даты заезда')

        if not self.is_room_available(room.id, check_in, check_out, exclude_id=serializer.instance.id):
            raise ValidationError(f'Номер {room.number} занят в выбранные даты')

        serializer.save()

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """История гостя"""
        client = self.get_object()
        all_stays = Client.objects.filter(
            passport_number=client.passport_number
        ).order_by('-check_in_date')
        serializer = self.get_serializer(all_stays, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my-bookings', permission_classes=[IsAuthenticated])
    def my_bookings(self, request):
        bookings = Client.objects.filter(booked_by=request.user).select_related('room').order_by('-check_in_date')
        data = []
        for client in bookings:
            data.append({
                'id': client.id,
                'room_number': client.room.number,
                'room_id': client.room_id,
                'room_type': client.room.get_room_type_display(),
                'price': str(client.room.price),
                'guest_name': f"{client.last_name} {client.first_name}",
                'passport_number': client.passport_number,
                'check_in_date': client.check_in_date,
                'check_out_date': client.check_out_date,
                'city_of_origin': client.city_of_origin,
            })
        return Response(data)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'dismissed']

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        employee = self.get_object()
        schedules = CleaningSchedule.objects.filter(employee=employee)
        data = []
        for s in schedules:
            data.append({
                'day': s.get_day_of_week_display(),
                'floor': s.floor
            })
        return Response(data)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room_type', 'floor']

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        room = self.get_object()
        qs = Client.objects.filter(room=room)
        if request.user.is_authenticated:
            qs = qs.filter(booked_by=request.user)
        else:
            qs = qs.none()
        data = []
        for client in qs:
            data.append({
                'name': f"{client.last_name} {client.first_name}",
                'from': client.check_in_date,
                'to': client.check_out_date
            })
        return Response(data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        today = timezone.now().date()
        occupied_rooms = Room.objects.filter(
            clients__check_in_date__lte=today,
            clients__check_out_date__gte=today
        ).distinct()
        available_rooms = Room.objects.exclude(id__in=occupied_rooms.values('id'))
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def current_guest(self, request, pk=None):
        room = self.get_object()
        today = timezone.now().date()
        guest = Client.objects.filter(
            room=room,
            check_in_date__lte=today,
            check_out_date__gte=today
        ).first()

        if guest:
            return Response({
                'name': f"{guest.last_name} {guest.first_name}",
                'passport': guest.passport_number,
                'check_in': guest.check_in_date,
                'check_out': guest.check_out_date
            })
        return Response({'message': 'номер свободен'})

class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'day_of_week']

