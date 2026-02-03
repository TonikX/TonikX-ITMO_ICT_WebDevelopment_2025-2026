"""
Views для REST API
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q, Count, Sum, F
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Room, Guest, Staff, CleaningSchedule
from .serializers import (
    RoomSerializer, GuestSerializer, GuestCreateSerializer, GuestCheckOutSerializer,
    StaffSerializer, StaffCreateSerializer, StaffFireSerializer,
    CleaningScheduleSerializer
)


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet для номеров"""
    
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['number', 'phone']
    ordering_fields = ['number', 'floor', 'price_per_day']
    
    def destroy(self, request, *args, **kwargs):
        """Удаление номера с проверкой связанных записей"""
        instance = self.get_object()
        
        # Проверяем наличие текущих гостей (без check_out_date)
        current_guests = instance.guests.filter(check_out_date__isnull=True)
        if current_guests.exists():
            return Response(
                {
                    'error': f'Невозможно удалить номер {instance.number}. '
                             f'В номере проживают {current_guests.count()} гостей. '
                             f'Сначала необходимо выселить или переместить всех гостей.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Удаляем исторические записи гостей (уже выселенных)
        # Это необходимо, так как on_delete=models.PROTECT блокирует удаление Room
        historical_guests = instance.guests.filter(check_out_date__isnull=False)
        historical_count = historical_guests.count()
        if historical_count > 0:
            historical_guests.delete()
        
        # Теперь можно безопасно удалить номер
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Получить список свободных номеров"""
        available_rooms = []
        for room in self.queryset:
            if room.is_available():
                available_rooms.append(room)
        
        serializer = self.get_serializer(available_rooms, many=True)
        return Response({
            'count': len(available_rooms),
            'rooms': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def guests_history(self, request, pk=None):
        """История клиентов в номере"""
        room = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        guests = room.guests.all()
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                guests = guests.filter(
                    Q(check_out_date__isnull=True) | Q(check_out_date__gte=start_date)
                )
            except ValueError:
                return Response(
                    {'error': 'Неверный формат даты start_date. Используйте YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                guests = guests.filter(check_in_date__lte=end_date)
            except ValueError:
                return Response(
                    {'error': 'Неверный формат даты end_date. Используйте YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = GuestSerializer(guests, many=True)
        return Response({
            'room': RoomSerializer(room).data,
            'guests': serializer.data,
            'count': guests.count()
        })


class GuestViewSet(viewsets.ModelViewSet):
    """ViewSet для клиентов"""
    
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['passport_number', 'last_name', 'first_name', 'city']
    ordering_fields = ['check_in_date', 'check_out_date', 'last_name']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create' or self.action == 'check_in':
            return GuestCreateSerializer
        elif self.action == 'check_out':
            return GuestCheckOutSerializer
        return GuestSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Список текущих гостей"""
        today = timezone.now().date()
        current_guests = self.queryset.filter(
            check_in_date__lte=today
        ).filter(
            Q(check_out_date__isnull=True) | Q(check_out_date__gte=today)
        )
        
        serializer = self.get_serializer(current_guests, many=True)
        return Response({
            'count': current_guests.count(),
            'guests': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def from_city(self, request):
        """Клиенты из заданного города"""
        city = request.query_params.get('city')
        if not city:
            return Response(
                {'error': 'Параметр city обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        guests = self.queryset.filter(city__icontains=city)
        serializer = self.get_serializer(guests, many=True)
        
        return Response({
            'city': city,
            'count': guests.count(),
            'guests': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def cleaning_staff(self, request, pk=None):
        """Кто убирал номер клиента в заданный день недели"""
        guest = self.get_object()
        weekday = request.query_params.get('weekday')
        
        if not weekday:
            return Response(
                {'error': 'Параметр weekday обязателен (1-7)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            weekday = int(weekday)
            if weekday < 1 or weekday > 7:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Параметр weekday должен быть числом от 1 до 7'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Находим расписание уборки для этажа номера гостя в указанный день
        schedules = CleaningSchedule.objects.filter(
            floor=guest.room.floor,
            weekday=weekday,
            staff__is_active=True
        )
        
        serializer = CleaningScheduleSerializer(schedules, many=True)
        
        return Response({
            'guest': GuestSerializer(guest).data,
            'weekday': weekday,
            'cleaning_staff': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def concurrent_guests(self, request, pk=None):
        """Клиенты, проживавшие одновременно с заданным"""
        guest = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Определяем период для поиска
        if start_date:
            try:
                search_start = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Неверный формат start_date. Используйте YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            search_start = guest.check_in_date
        
        if end_date:
            try:
                search_end = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Неверный формат end_date. Используйте YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            search_end = guest.check_out_date or timezone.now().date()
        
        # Находим пересекающихся гостей
        concurrent_guests = Guest.objects.filter(
            check_in_date__lte=search_end
        ).filter(
            Q(check_out_date__isnull=True) | Q(check_out_date__gte=search_start)
        ).exclude(id=guest.id)
        
        serializer = self.get_serializer(concurrent_guests, many=True)
        
        return Response({
            'guest': GuestSerializer(guest).data,
            'period': {
                'start': search_start,
                'end': search_end
            },
            'concurrent_guests': serializer.data,
            'count': concurrent_guests.count()
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def check_in(self, request):
        """Поселить клиента"""
        serializer = GuestCreateSerializer(data=request.data)
        if serializer.is_valid():
            guest = serializer.save()
            return Response(
                GuestSerializer(guest).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def check_out(self, request, pk=None):
        """Выселить клиента"""
        guest = self.get_object()
        
        if guest.check_out_date:
            return Response(
                {'error': 'Клиент уже выселен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = GuestCheckOutSerializer(guest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(GuestSerializer(guest).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffViewSet(viewsets.ModelViewSet):
    """ViewSet для служащих"""
    
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        """Удаление служащего с проверкой связанных записей"""
        instance = self.get_object()
        
        # Проверяем наличие связанных расписаний
        if instance.schedules.exists():
            return Response(
                {
                    'error': f'Невозможно удалить служащего {instance.full_name}. '
                             f'У служащего есть связанные расписания уборки. '
                             f'Сначала необходимо удалить или изменить расписания.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['last_name', 'first_name', 'middle_name']
    ordering_fields = ['last_name', 'hire_date']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create' or self.action == 'hire':
            return StaffCreateSerializer
        elif self.action == 'fire':
            return StaffFireSerializer
        return StaffSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Список работающих служащих"""
        active_staff = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_staff, many=True)
        return Response({
            'count': active_staff.count(),
            'staff': serializer.data
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def hire(self, request):
        """Принять служащего на работу"""
        serializer = StaffCreateSerializer(data=request.data)
        if serializer.is_valid():
            staff = serializer.save(is_active=True)
            return Response(
                StaffSerializer(staff).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def fire(self, request, pk=None):
        """Уволить служащего"""
        staff = self.get_object()
        
        if not staff.is_active:
            return Response(
                {'error': 'Служащий уже уволен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = StaffFireSerializer(staff, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(is_active=False)
            return Response(StaffSerializer(staff).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet для расписания уборки"""
    
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['weekday', 'floor']
    
    @action(detail=False, methods=['get'])
    def by_floor(self, request):
        """Расписание уборки по этажу"""
        floor = request.query_params.get('floor')
        
        if not floor:
            return Response(
                {'error': 'Параметр floor обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            floor = int(floor)
        except ValueError:
            return Response(
                {'error': 'Параметр floor должен быть числом'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        schedules = self.queryset.filter(floor=floor, staff__is_active=True)
        serializer = self.get_serializer(schedules, many=True)
        
        return Response({
            'floor': floor,
            'schedules': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def by_weekday(self, request):
        """Расписание уборки по дню недели"""
        weekday = request.query_params.get('weekday')
        
        if not weekday:
            return Response(
                {'error': 'Параметр weekday обязателен (1-7)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            weekday = int(weekday)
            if weekday < 1 or weekday > 7:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Параметр weekday должен быть числом от 1 до 7'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        schedules = self.queryset.filter(weekday=weekday, staff__is_active=True)
        serializer = self.get_serializer(schedules, many=True)
        
        return Response({
            'weekday': weekday,
            'schedules': serializer.data
        })


class ReportViewSet(viewsets.ViewSet):
    """ViewSet для отчетов"""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def quarterly(self, request):
        """Отчет за квартал"""
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')
        
        if not year or not quarter:
            return Response(
                {'error': 'Параметры year и quarter обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            year = int(year)
            quarter = int(quarter)
            if quarter < 1 or quarter > 4:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'year должен быть числом, quarter от 1 до 4'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Определяем даты квартала
        quarter_start_months = {1: 1, 2: 4, 3: 7, 4: 10}
        start_month = quarter_start_months[quarter]
        start_date = datetime(year, start_month, 1).date()
        
        if quarter == 4:
            end_date = datetime(year, 12, 31).date()
        else:
            end_month = start_month + 2
            # Последний день месяца
            if end_month in [1, 3, 5, 7, 8, 10, 12]:
                end_date = datetime(year, end_month, 31).date()
            elif end_month in [4, 6, 9, 11]:
                end_date = datetime(year, end_month, 30).date()
            else:  # февраль
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                    end_date = datetime(year, end_month, 29).date()
                else:
                    end_date = datetime(year, end_month, 28).date()
        
        # Собираем статистику
        rooms = Room.objects.all()
        report_data = []
        total_income = 0
        
        for room in rooms:
            # Гости в этом номере за период
            guests = Guest.objects.filter(
                room=room,
                check_in_date__lte=end_date
            ).filter(
                Q(check_out_date__isnull=True) | Q(check_out_date__gte=start_date)
            )
            
            # Подсчет дохода
            room_income = 0
            for guest in guests:
                # Определяем период проживания в пределах квартала
                stay_start = max(guest.check_in_date, start_date)
                stay_end = min(
                    guest.check_out_date if guest.check_out_date else end_date,
                    end_date
                )
                days = (stay_end - stay_start).days + 1
                room_income += days * float(room.price_per_day)
            
            total_income += room_income
            
            report_data.append({
                'room_number': room.number,
                'room_type': room.get_room_type_display(),
                'floor': room.floor,
                'guests_count': guests.count(),
                'income': room_income
            })
        
        # Количество номеров на каждом этаже
        floors_stat = Room.objects.values('floor').annotate(
            rooms_count=Count('id')
        ).order_by('floor')
        
        return Response({
            'period': {
                'year': year,
                'quarter': quarter,
                'start_date': start_date,
                'end_date': end_date
            },
            'rooms': report_data,
            'floors_statistics': list(floors_stat),
            'total_income': total_income,
            'total_rooms': rooms.count()
        })
