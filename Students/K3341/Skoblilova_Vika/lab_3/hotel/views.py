from django.shortcuts import render
from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from .models import Guest, Room, Employee, Booking, CleaningSchedule, Transaction
from .serializers import *


class GuestViewSet(viewsets.ModelViewSet):
    """API для работы с гостями"""
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def by_city(self, request):
        """Гости из определенного города"""
        city = request.query_params.get('city')
        if city:
            guests = Guest.objects.filter(city__icontains=city)
            serializer = self.get_serializer(guests, many=True)
            return Response(serializer.data)
        return Response({"error": "Укажите параметр city"}, status=400)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Активные гости (сейчас проживающие)"""
        today = timezone.now().date()
        active_guests = Guest.objects.filter(
            bookings__check_in_date__lte=today,
            bookings__check_out_date__gte=today,
            bookings__status='checked_in'
        ).distinct()
        serializer = self.get_serializer(active_guests, many=True)
        return Response(serializer.data)


class RoomViewSet(viewsets.ModelViewSet):
    """API для работы с номерами"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Свободные номера на определенные даты"""
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')

        if not check_in or not check_out:
            return Response({"error": "Укажите check_in и check_out"}, status=400)

        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Неверный формат даты. Используйте YYYY-MM-DD"}, status=400)

        # Номера, которые заняты в указанный период
        occupied_rooms = Booking.objects.filter(
            Q(check_in_date__lt=check_out_date) & Q(check_out_date__gt=check_in_date),
            status__in=['confirmed', 'checked_in']
        ).values_list('room_id', flat=True)

        # Свободные номера
        available_rooms = Room.objects.exclude(id__in=occupied_rooms).filter(status='free')
        serializer = self.get_serializer(available_rooms, many=True)

        return Response({
            'check_in': check_in_date,
            'check_out': check_out_date,
            'available_rooms': len(available_rooms),
            'rooms': serializer.data
        })

    @action(detail=False, methods=['get'])
    def by_floor(self, request):
        """Номера по этажу"""
        floor = request.query_params.get('floor')
        if floor:
            rooms = Room.objects.filter(floor=floor)
            serializer = self.get_serializer(rooms, many=True)
            return Response(serializer.data)
        return Response({"error": "Укажите параметр floor"}, status=400)


class EmployeeViewSet(viewsets.ModelViewSet):
    """API для работы с сотрудниками"""
    queryset = Employee.objects.filter(dismissal_date__isnull=True)
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Уволить сотрудника"""
        employee = self.get_object()
        employee.dismissal_date = timezone.now().date()
        employee.save()
        return Response({"message": f"Сотрудник {employee.last_name} уволен"})

    @action(detail=False, methods=['get'])
    def schedule(self, request):
        """Расписание уборки сотрудников"""
        day = request.query_params.get('day')
        if day:
            schedules = CleaningSchedule.objects.filter(cleaning_day=day)
            serializer = CleaningScheduleSerializer(schedules, many=True)
            return Response(serializer.data)
        return Response({"error": "Укажите параметр day"}, status=400)


class BookingViewSet(viewsets.ModelViewSet):
    """API для работы с бронированиями"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Автоматический расчет стоимости при создании бронирования"""
        booking = serializer.save()
        days = (booking.check_out_date - booking.check_in_date).days
        total_cost = booking.room.price_per_day * days
        booking.total_cost = total_cost
        booking.save()

        # Создаем транзакцию
        Transaction.objects.create(
            booking=booking,
            amount=total_cost,
            transaction_type='payment'
        )

    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        """Заселить гостя"""
        booking = self.get_object()
        booking.status = 'checked_in'
        booking.save()

        # Меняем статус номера
        room = booking.room
        room.status = 'occupied'
        room.save()

        return Response({"message": "Гость успешно заселен"})

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        """Выселить гостя"""
        booking = self.get_object()
        booking.status = 'checked_out'
        booking.save()

        # Меняем статус номера
        room = booking.room
        room.status = 'free'
        room.save()

        return Response({"message": "Гость успешно выселен"})

    @action(detail=False, methods=['get'])
    def by_period(self, request):
        """Бронирования за период"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Укажите start_date и end_date"}, status=400)

        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Неверный формат даты. Используйте YYYY-MM-DD"}, status=400)

        bookings = Booking.objects.filter(
            check_in_date__lte=end,
            check_out_date__gte=start
        )
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    """API для работы с расписанием уборки"""
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def for_room(self, request):
        """Расписание уборки для номера"""
        room_id = request.query_params.get('room_id')
        if room_id:
            schedules = CleaningSchedule.objects.filter(room_id=room_id)
            serializer = self.get_serializer(schedules, many=True)
            return Response(serializer.data)
        return Response({"error": "Укажите параметр room_id"}, status=400)


class ReportView(APIView):
    """API для генерации отчетов"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        report_type = request.query_params.get('type')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not report_type:
            return Response({"error": "Укажите тип отчета (type)"}, status=400)

        # Отчет за квартал
        if report_type == 'quarterly':
            if not start_date or not end_date:
                return Response({"error": "Для квартального отчета укажите start_date и end_date"}, status=400)

            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Неверный формат даты"}, status=400)

            # 1. Число клиентов за период в каждом номере
            room_stats = Booking.objects.filter(
                check_in_date__lte=end,
                check_out_date__gte=start
            ).values('room__room_number', 'room__room_type').annotate(
                client_count=Count('guest', distinct=True),
                total_income=Sum('total_cost'),
                booking_count=Count('id')
            )

            # 2. Количество номеров на каждом этаже
            floor_stats = Room.objects.values('floor').annotate(
                room_count=Count('id'),
                free_rooms=Count('id', filter=Q(status='free'))
            )

            # 3. Общая сумма дохода
            total_income = Booking.objects.filter(
                check_in_date__lte=end,
                check_out_date__gte=start
            ).aggregate(total=Sum('total_cost'))['total'] or 0

            return Response({
                'period': f"{start} - {end}",
                'room_statistics': list(room_stats),
                'floor_statistics': list(floor_stats),
                'total_income': total_income
            })

        # Отчет по свободным номерам
        elif report_type == 'available_rooms':
            available_rooms = Room.objects.filter(status='free')
            serializer = RoomSerializer(available_rooms, many=True)
            return Response({
                'available_rooms_count': available_rooms.count(),
                'rooms': serializer.data
            })

        return Response({"error": "Неизвестный тип отчета"}, status=400)
