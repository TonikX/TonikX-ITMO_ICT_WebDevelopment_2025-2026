from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Room, Guest, Stay, Employee, CleaningSchedule
from .serializers import (
    RoomSerializer, GuestSerializer, StaySerializer,
    EmployeeSerializer, CleaningScheduleSerializer
)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['room_type', 'floor', 'is_occupied']
    search_fields = ['number', 'phone']
    ordering_fields = ['number', 'floor', 'price_per_night']
    ordering = ['floor', 'number']
    
    @swagger_auto_schema(
        operation_description="Список свободных номеров",
        responses={200: RoomSerializer(many=True)},
        tags=['Номера']
    )
    @action(detail=False, methods=['get'])
    def available(self, request):
        rooms = self.queryset.filter(is_occupied=False)
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Номера по типу",
        manual_parameters=[
            openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: RoomSerializer(many=True)},
        tags=['Номера']
    )
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        room_type = request.query_params.get('type')
        if not room_type:
            return Response({'error': 'Не указан тип'}, status=status.HTTP_400_BAD_REQUEST)
        rooms = self.queryset.filter(room_type=room_type)
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city']
    search_fields = ['last_name', 'first_name', 'middle_name', 'passport_number', 'city']
    ordering_fields = ['last_name', 'first_name', 'city']
    ordering = ['last_name', 'first_name']
    
    @swagger_auto_schema(
        operation_description="Клиенты по городу",
        manual_parameters=[
            openapi.Parameter('city', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: GuestSerializer(many=True)},
        tags=['Клиенты']
    )
    @action(detail=False, methods=['get'])
    def by_city(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'error': 'Не указан город'}, status=status.HTTP_400_BAD_REQUEST)
        guests = self.queryset.filter(city__icontains=city)
        serializer = self.get_serializer(guests, many=True)
        return Response(serializer.data)


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.select_related('guest', 'room').all()
    serializer_class = StaySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['room', 'guest']
    ordering_fields = ['check_in_date', 'check_out_date']
    ordering = ['-check_in_date']
    
    @swagger_auto_schema(
        operation_description="Клиенты в номере за период",
        manual_parameters=[
            openapi.Parameter('room_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
        ],
        responses={200: StaySerializer(many=True)},
        tags=['Проживания']
    )
    @action(detail=False, methods=['get'])
    def by_room(self, request):
        room_id = request.query_params.get('room_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not room_id:
            return Response({'error': 'Не указан номер'}, status=status.HTTP_400_BAD_REQUEST)
        
        stays = self.queryset.filter(room_id=room_id)
        
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                stays = stays.filter(check_in_date__gte=start)
            except:
                return Response({'error': 'Неверный формат даты'}, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                stays = stays.filter(check_in_date__lte=end)
            except:
                return Response({'error': 'Неверный формат даты'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(stays, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Текущие проживания",
        responses={200: StaySerializer(many=True)},
        tags=['Проживания']
    )
    @action(detail=False, methods=['get'])
    def current(self, request):
        stays = self.queryset.filter(check_out_date__isnull=True)
        serializer = self.get_serializer(stays, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Проживания за период",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: StaySerializer(many=True)},
        tags=['Проживания']
    )
    @action(detail=False, methods=['get'])
    def by_period(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response({'error': 'Не указаны даты'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            stays = self.queryset.filter(
                Q(check_in_date__lte=end) & (Q(check_out_date__isnull=True) | Q(check_out_date__gte=start))
            )
            serializer = self.get_serializer(stays, many=True)
            return Response(serializer.data)
        except:
            return Response({'error': 'Неверный формат даты'}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['last_name', 'first_name', 'middle_name']
    ordering_fields = ['last_name', 'first_name']
    ordering = ['last_name', 'first_name']
    
    @swagger_auto_schema(
        operation_description="Активные служащие",
        responses={200: EmployeeSerializer(many=True)},
        tags=['Служащие']
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        employees = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data)


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.select_related('employee').all()
    serializer_class = CleaningScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'floor', 'day_of_week']
    ordering_fields = ['day_of_week', 'floor']
    ordering = ['day_of_week', 'floor']
    
    @swagger_auto_schema(
        operation_description="Кто убирал номер клиента",
        manual_parameters=[
            openapi.Parameter('guest_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('day_of_week', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: CleaningScheduleSerializer(many=True)},
        tags=['Расписание уборки']
    )
    @action(detail=False, methods=['get'])
    def by_guest_room(self, request):
        guest_id = request.query_params.get('guest_id')
        day_of_week = request.query_params.get('day_of_week')
        
        if not guest_id or not day_of_week:
            return Response({'error': 'Не указаны параметры'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            stay = Stay.objects.filter(guest_id=guest_id, check_out_date__isnull=True).first()
            if not stay:
                return Response({'error': 'Клиент не найден'}, status=status.HTTP_404_NOT_FOUND)
            
            schedules = self.queryset.filter(floor=stay.room.floor, day_of_week=day_of_week)
            serializer = self.get_serializer(schedules, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
