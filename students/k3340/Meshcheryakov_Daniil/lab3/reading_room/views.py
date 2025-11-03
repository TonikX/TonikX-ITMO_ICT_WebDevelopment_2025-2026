from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Count, Q
from django.utils.dateparse import parse_datetime, parse_date
from rest_framework import viewsets, permissions, decorators, response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import ReadingRoom, Reader, Reservation, Librarian, Schedule
from .serializers import (
    ReadingRoomSerializer,
    ReaderSerializer,
    ReservationSerializer,
    LibrarianSerializer,
    ScheduleSerializer,
    ReaderListItemSerializer,
)


# ===== СИСТЕМА ПРАВ ДОСТУПА =====

# Класс прав доступа: чтение для всех, изменение только для администраторов
# Используется для ограничения доступа к CRUD операциям
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.user and request.user.is_staff

# Класс прав доступа: все операции доступны авторизованным пользователям
class IsAuthenticatedForAll(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ ЧИТАЛЬНЫХ ЗАЛОВ =====

# ViewSet для управления читальными залами
# Предоставляет полный CRUD функционал + дополнительные действия
@extend_schema_view(
    list=extend_schema(summary="Список залов", description="Получить список всех читальных залов"),
    create=extend_schema(summary="Создать зал", description="Создать новый читальный зал (только для администраторов)"),
    retrieve=extend_schema(summary="Детали зала", description="Получить информацию о конкретном зале"),
    update=extend_schema(summary="Обновить зал", description="Обновить информацию о зале (только для администраторов)"),
    destroy=extend_schema(summary="Удалить зал", description="Удалить зал (только для администраторов)"),
)
class ReadingRoomViewSet(viewsets.ModelViewSet):
    queryset = ReadingRoom.objects.all()
    serializer_class = ReadingRoomSerializer
    permission_classes = [IsAuthenticatedForAll]

    # Дополнительное действие: поиск свободных залов на дату/время
    # Используется для проверки доступности залов при бронировании
    @extend_schema(
        summary="Свободные залы",
        description="Получить список свободных залов на указанную дату/время",
        parameters=[
            OpenApiParameter(
                name='on',
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description='Дата и время для проверки (YYYY-MM-DDTHH:MM:SS). По умолчанию - сейчас',
                required=False
            )
        ]
    )
    @decorators.action(detail=False, methods=["get"], url_path="free")
    def free_reading_rooms(self, request):
        """Свободные залы на дату/время (?on=YYYY-MM-DDTHH:MM:SS)"""
        on_str = request.query_params.get("on")
        if on_str:
            on = parse_datetime(on_str) or datetime.now()
        else:
            on = datetime.now()
        
        busy_reservations = Reservation.objects.filter(
            reserved_from__lte=on,
            is_active=True
        ).filter(
            Q(reserved_to__isnull=True) | Q(reserved_to__gt=on)
        )
        busy = busy_reservations.values_list("reading_room_id", flat=True)
        free = ReadingRoom.objects.exclude(id__in=busy)
        return response.Response({
            "datetime": on.isoformat(),
            "free_count": free.count(),
            "free_reading_rooms": ReadingRoomSerializer(free, many=True).data
        })

    # Дополнительное действие: читатели, бронировавшие зал за период
    # Используется для аналитики и отчетов по конкретному залу
    @decorators.action(detail=True, methods=["get"], url_path="readers")
    def readers_in_period(self, request, pk=None):
        """Читатели, бронировавшие зал за период ?start&end"""
        reading_room = self.get_object()
        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")
        
        if not start_str or not end_str:
            return response.Response({"detail": "start и end обязательны (формат: YYYY-MM-DDTHH:MM:SS)"}, status=400)
        
        start = parse_datetime(start_str)
        end = parse_datetime(end_str)
        
        if not start or not end:
            return response.Response({"detail": "Неверный формат даты (используйте YYYY-MM-DDTHH:MM:SS)"}, status=400)
        
        reservations = Reservation.objects.filter(reading_room=reading_room).filter(
            reserved_from__lte=end
        ).filter(
            Q(reserved_to__isnull=True) | Q(reserved_to__gte=start)
        )
        readers = Reader.objects.filter(reservations__in=reservations.values_list('id', flat=True)).distinct()
        return response.Response(ReaderListItemSerializer(readers, many=True).data)


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ ЧИТАТЕЛЕЙ =====

# ViewSet для управления читателями
# Предоставляет полный CRUD функционал + аналитические действия
class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    permission_classes = [IsAuthenticatedForAll]

    # Дополнительное действие: подсчет читателей по телефону
    # Используется для статистики и аналитики
    @decorators.action(detail=False, methods=["get"], url_path="count-by-phone")
    def count_by_phone(self, request):
        phone = request.query_params.get("phone")
        if not phone:
            return response.Response({"detail": "phone обязателен"}, status=400)
        count = Reader.objects.filter(phone__icontains=phone).count()
        return response.Response({"phone": phone, "count": count})

    # Дополнительное действие: кто работал на этаже читателя в определенный день недели
    # Используется для определения ответственного библиотекаря
    @decorators.action(detail=True, methods=["get"], url_path="librarian")
    def librarian_on_weekday(self, request, pk=None):
        """Кто работал на этаже читателя в день недели (?weekday=1..7)"""
        reader = self.get_object()
        weekday = int(request.query_params.get("weekday", 0))
        if weekday not in range(1, 8):
            return response.Response({"detail": "weekday 1..7"}, status=400)
        reservation = reader.reservations.order_by("-reserved_from").first()
        if not reservation:
            return response.Response({"detail": "Нет данных о бронировании"}, status=404)
        librarians = Librarian.objects.filter(
            schedules__weekday=weekday,
            schedules__floor=reservation.reading_room.floor,
            is_active=True,
        ).distinct()
        return response.Response(LibrarianSerializer(librarians, many=True).data)

    # Дополнительное действие: читатели, бронировавшие одновременно с указанным читателем
    # Используется для поиска потенциальных контактов и аналитики пересечений
    @decorators.action(detail=True, methods=["get"], url_path="co-readers")
    def co_readers(self, request, pk=None):
        """Читатели, бронировавшие в те же дни, что и указанный читатель"""
        reader = self.get_object()
        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")
        
        if not start_str or not end_str:
            return response.Response({"detail": "start и end обязательны (формат: YYYY-MM-DDTHH:MM:SS)"}, status=400)
        
        start = parse_datetime(start_str)
        end = parse_datetime(end_str)
        
        if not start or not end:
            return response.Response({"detail": "Неверный формат даты"}, status=400)
        
        overlapping = Reservation.objects.filter(
            reserved_from__lte=end
        ).filter(
            Q(reserved_to__isnull=True) | Q(reserved_to__gte=start)
        ).exclude(reader=reader)
        readers = Reader.objects.filter(reservations__in=overlapping.values_list('id', flat=True)).distinct()
        return response.Response(ReaderListItemSerializer(readers, many=True).data)


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ БРОНИРОВАНИЙ =====

# ViewSet для управления бронированиями читателей
# Предоставляет полный CRUD функционал для регистрации бронирований
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("reader", "reading_room")
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticatedForAll]


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ БИБЛИОТЕКАРЕЙ =====

# ViewSet для управления библиотекарями
# Предоставляет полный CRUD функционал + действия для приема/увольнения
class LibrarianViewSet(viewsets.ModelViewSet):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer
    permission_classes = [IsAuthenticatedForAll]

    # Дополнительное действие: увольнение библиотекаря
    # Устанавливает статус is_active = False
    @decorators.action(detail=True, methods=["post"], url_path="fire")
    def fire(self, request, pk=None):
        librarian = self.get_object()
        librarian.is_active = False
        librarian.save(update_fields=["is_active"])
        return response.Response(LibrarianSerializer(librarian).data)

    # Дополнительное действие: прием библиотекаря на работу
    # Устанавливает статус is_active = True
    @decorators.action(detail=True, methods=["post"], url_path="hire")
    def hire(self, request, pk=None):
        librarian = self.get_object()
        librarian.is_active = True
        librarian.save(update_fields=["is_active"])
        return response.Response(LibrarianSerializer(librarian).data)


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ РАСПИСАНИЯ БИБЛИОТЕКАРЕЙ =====

# ViewSet для управления расписанием работы библиотекарей
# Предоставляет полный CRUD функционал для назначения библиотекарей на этажи по дням недели
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related("librarian")
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticatedForAll]


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ ОТЧЕТОВ =====

# API View для генерации квартальных отчетов
# Предоставляет детальную аналитику по доходам, читателям и загруженности залов
class QuarterReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Отчёт по кварталу ?quarter=1..4"""
        q = int(request.query_params.get("quarter", 1))
        year = datetime.now().year
        if q not in (1, 2, 3, 4):
            return response.Response({"detail": "quarter 1..4"}, status=400)

        q_start_month = (q - 1) * 3 + 1
        start = datetime(year, q_start_month, 1)
        end_month = (q_start_month + 3 - 1) % 12 + 1
        end_year = year + (q == 4)
        end = datetime(end_year, end_month, 1) - timedelta(seconds=1)

        # Кол-во читателей по каждому залу
        reading_room_reader_counts = []
        for reading_room in ReadingRoom.objects.all():
            c = Reader.objects.filter(
                reservations__reading_room=reading_room,
                reservations__reserved_from__lte=end,
                reservations__reserved_to__gte=start,
                reservations__is_active=True
            ).distinct().count()
            reading_room_reader_counts.append({"reading_room": reading_room.number, "readers": c})

        # Количество залов на этажах
        floors = ReadingRoom.objects.values("floor").annotate(count=Count("id")).order_by("floor")

        # Доход
        def overlap_hours(r: Reservation, start, end):
            r_end = r.reserved_to or end
            a = max(r.reserved_from, start)
            b = min(r_end, end)
            if a >= b:
                return 0
            delta = b - a
            return max(0, delta.total_seconds() / 3600)  # Конвертируем в часы

        total_income = Decimal("0")
        reading_room_income = []
        for reading_room in ReadingRoom.objects.all():
            reservations = Reservation.objects.filter(
                reading_room=reading_room, 
                reserved_from__lte=end,
                is_active=True
            ).filter(
                Q(reserved_to__isnull=True) | Q(reserved_to__gte=start)
            )
            income = sum(Decimal(str(reading_room.hourly_rate)) * Decimal(str(overlap_hours(r, start, end))) for r in reservations)
            total_income += income
            reading_room_income.append({"reading_room": reading_room.number, "income": income})

        return response.Response({
            "period": {"start": start.isoformat(), "end": end.isoformat()},
            "readers_per_room": reading_room_reader_counts,
            "rooms_per_floor": list(floors),
            "income_per_room": reading_room_income,
            "total_income": total_income,
        })

