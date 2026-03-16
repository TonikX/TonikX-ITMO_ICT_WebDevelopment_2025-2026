from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta

from hotel.models import Room, Client, Employee, CleaningSchedule
from api.serializers import (
    RoomSerializer, ClientSerializer, EmployeeSerializer, CleaningScheduleSerializer,
    RoomClientsPeriodSerializer, ClientSamePeriodSerializer
)

import django_filters


# -------------------- FILTERS --------------------

class RoomFilter(django_filters.FilterSet):
    room_type = django_filters.ChoiceFilter(choices=Room.ROOM_TYPES)
    floor = django_filters.NumberFilter()
    min_price = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='lte')

    class Meta:
        model = Room
        fields = ['room_type', 'floor', 'is_available']


class ClientFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='icontains')
    check_in_after = django_filters.DateFilter(field_name='check_in_date', lookup_expr='gte')
    check_in_before = django_filters.DateFilter(field_name='check_in_date', lookup_expr='lte')

    class Meta:
        model = Client
        fields = ['city', 'room']


# -------------------- VIEWSETS --------------------

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Свободные номера + сколько их (по ТЗ).
        """
        rooms = Room.objects.filter(is_available=True)
        serializer = self.get_serializer(rooms, many=True)
        return Response({
            "count": rooms.count(),
            "results": serializer.data
        })

    @action(detail=False, methods=['post'])
    def clients_in_period(self, request):
        """
        Клиенты, проживавшие в заданном номере, в заданный период времени (по ТЗ).
        Пересечение периодов:
        client.check_in <= end AND (client.check_out >= start OR check_out is null)
        """
        serializer = RoomClientsPeriodSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        room_id = serializer.validated_data['room_id']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        clients = Client.objects.filter(
            room_id=room_id,
            check_in_date__lte=end_date,
        ).filter(
            Q(check_out_date__gte=start_date) | Q(check_out_date__isnull=True)
        )

        return Response(ClientSerializer(clients, many=True).data)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter

    def perform_create(self, serializer):
        """
        Поселить клиента (по ТЗ):
        - создать запись клиента
        - если клиент не выселен (check_out_date is null) -> номер становится занятым
        """
        client = serializer.save()
        if client.check_out_date is None:
            room = client.room
            room.is_available = False
            room.save()

    @action(detail=False, methods=['get'])
    def from_city(self, request):
        """
        Количество клиентов, прибывших из заданного города (по ТЗ).
        """
        city = request.query_params.get('city')
        if not city:
            return Response({'error': 'Укажите параметр city'}, status=status.HTTP_400_BAD_REQUEST)

        count = Client.objects.filter(city__iexact=city).count()
        return Response({'city': city, 'count': count})

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        """
        Выселить клиента (по ТЗ):
        - ставим дату выселения
        - освобождаем номер
        """
        client = self.get_object()
        raw = request.data.get('check_out_date')

        if raw:
            dt = parse_date(raw)
            if not dt:
                return Response(
                    {'error': 'Неверный формат check_out_date. Используйте YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            check_out_date = dt
        else:
            check_out_date = timezone.now().date()

        client.check_out_date = check_out_date
        client.save()

        room = client.room
        room.is_available = True
        room.save()

        return Response({
            'status': 'клиент выселен',
            'client_id': client.id,
            'check_out_date': client.check_out_date,
            'room_number': room.number,
            'room_status': 'свободен'
        })

    @action(detail=False, methods=['post'])
    def same_period_clients(self, request):
        """
        Список клиентов с городом, которые проживали в те же дни, что и заданный клиент,
        в определенный период времени (по ТЗ).
        """
        serializer = ClientSamePeriodSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_id = serializer.validated_data['client_id']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        try:
            Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Клиент не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Ищем клиентов, чьи периоды пересекаются с заданным интервалом
        clients = Client.objects.exclude(id=client_id).filter(
            Q(check_in_date__lte=end_date) &
            (
                Q(check_out_date__gte=start_date) |
                Q(check_out_date__isnull=True)
            )
        ).select_related('room')

        result = [{
            'id': c.id,
            'full_name': f"{c.last_name} {c.first_name}",
            'city': c.city,
            'check_in': c.check_in_date,
            'check_out': c.check_out_date,
            'room': c.room.number
        } for c in clients]

        return Response(result)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=True, methods=['post'])
    def fire(self, request, pk=None):
        """Уволить сотрудника (по ТЗ)"""
        employee = self.get_object()
        employee.is_active = False
        employee.save()
        return Response({'status': 'сотрудник уволен'})

    @action(detail=True, methods=['post'])
    def hire(self, request, pk=None):
        """Принять обратно на работу (по ТЗ)"""
        employee = self.get_object()
        employee.is_active = True
        employee.save()
        return Response({'status': 'сотрудник нанят'})

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Список активных сотрудников"""
        employees = Employee.objects.filter(is_active=True)
        return Response(self.get_serializer(employees, many=True).data)

    @action(detail=False, methods=['get'])
    def who_cleaned_client_room(self, request):
        """
        Кто из служащих убирал номер указанного клиента в заданный день недели (по ТЗ).
        GET /api/employees/who_cleaned_client_room/?client_id=1&day=mon
        day: mon,tue,wed,thu,fri,sat,sun
        """
        client_id = request.query_params.get('client_id')
        day_of_week = request.query_params.get('day')

        if not client_id or not day_of_week:
            return Response(
                {'error': 'Укажите параметры client_id и day'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            client = Client.objects.select_related('room').get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Клиент не найден'}, status=status.HTTP_404_NOT_FOUND)

        schedules = CleaningSchedule.objects.filter(
            floor=client.room.floor,
            day_of_week=day_of_week
        ).select_related('employee')

        result = [{
            'employee_id': s.employee.id,
            'employee_name': str(s.employee),
            'floor': s.floor,
            'day_of_week': s.get_day_of_week_display(),
            'client': {
                'id': client.id,
                'name': f"{client.last_name} {client.first_name}",
                'room_number': client.room.number,
                'room_floor': client.room.floor,
            }
        } for s in schedules]

        return Response(result)


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer


# -------------------- REPORT --------------------

class ReportView(generics.GenericAPIView):
    """
    Автоматическая выдача отчета за квартал (по ТЗ).
    GET /api/report/?quarter=4&year=2024
    """

    def get(self, request):
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')

        if not quarter or not year:
            return Response({'error': 'Необходимы параметры quarter и year'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quarter = int(quarter)
            year = int(year)
        except ValueError:
            return Response({'error': 'quarter и year должны быть числами'}, status=status.HTTP_400_BAD_REQUEST)

        if quarter not in [1, 2, 3, 4]:
            return Response({'error': 'Квартал должен быть 1, 2, 3 или 4'}, status=status.HTTP_400_BAD_REQUEST)

        # период квартала
        month_start = (quarter - 1) * 3 + 1
        start_date = datetime(year, month_start, 1).date()

        if quarter == 4:
            end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(year, month_start + 3, 1).date() - timedelta(days=1)

        # 1) число клиентов за период в каждом номере
        clients_by_room = Client.objects.filter(
            check_in_date__lte=end_date
        ).filter(
            Q(check_out_date__gte=start_date) | Q(check_out_date__isnull=True)
        ).values('room__number', 'room__room_type').annotate(
            client_count=Count('id')
        ).order_by('room__number')

        # 2) количество номеров на каждом этаже
        rooms_by_floor = Room.objects.values('floor').annotate(
            room_count=Count('id')
        ).order_by('floor')

        # 3) общая сумма дохода за каждый номер + 4) суммарный доход по гостинице
        income_by_room = []
        total_income = 0

        rooms = Room.objects.all()
        for room in rooms:
            room_clients = Client.objects.filter(
                room=room,
                check_in_date__lte=end_date
            ).filter(
                Q(check_out_date__gte=start_date) | Q(check_out_date__isnull=True)
            )

            room_income = 0
            for client in room_clients:
                days = self._days_in_period(
                    client.check_in_date,
                    client.check_out_date or timezone.now().date(),
                    start_date,
                    end_date
                )
                room_income += days * room.price_per_day

            income_by_room.append({
                'room_number': room.number,
                'room_type': room.get_room_type_display(),
                'floor': room.floor,
                'income': float(room_income),
            })
            total_income += room_income

        report = {
            'period': f'{year} Q{quarter}',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'clients_by_room': list(clients_by_room),
            'rooms_by_floor': list(rooms_by_floor),
            'income_by_room': income_by_room,
            'total_income': float(total_income),
            'generated_at': timezone.now().isoformat()
        }

        return Response(report)

    def _days_in_period(self, check_in, check_out, period_start, period_end):
        """
        Количество дней проживания, попавших в указанный период (включительно).
        """
        start = max(check_in, period_start)
        end = min(check_out, period_end) if check_out else period_end
        if start > end:
            return 0
        return (end - start).days + 1
