from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
from rest_framework import viewsets, permissions, decorators, response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Room, Client, Stay, Employee, EmployeeSchedule
from .serializers import (
    RoomSerializer,
    ClientSerializer,
    StaySerializer,
    EmployeeSerializer,
    EmployeeScheduleSerializer,
    ClientListItemSerializer,
)


# ===== СИСТЕМА ПРАВ ДОСТУПА =====

# Класс прав доступа: чтение для всех, изменение только для администраторов
# Используется для ограничения доступа к CRUD операциям
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.user and request.user.is_staff


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ НОМЕРОВ =====

# ViewSet для управления номерами гостиницы
# Предоставляет полный CRUD функционал + дополнительные действия
@extend_schema_view(
    list=extend_schema(summary="Список номеров", description="Получить список всех номеров гостиницы"),
    create=extend_schema(summary="Создать номер", description="Создать новый номер (только для администраторов)"),
    retrieve=extend_schema(summary="Детали номера", description="Получить информацию о конкретном номере"),
    update=extend_schema(summary="Обновить номер", description="Обновить информацию о номере (только для администраторов)"),
    destroy=extend_schema(summary="Удалить номер", description="Удалить номер (только для администраторов)"),
)
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Дополнительное действие: поиск свободных номеров на дату
    # Используется для проверки доступности номеров при бронировании
    @extend_schema(
        summary="Свободные номера",
        description="Получить список свободных номеров на указанную дату",
        parameters=[
            OpenApiParameter(
                name='on',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Дата для проверки (YYYY-MM-DD). По умолчанию - сегодня',
                required=False
            )
        ]
    )
    @decorators.action(detail=False, methods=["get"], url_path="free")
    def free_rooms(self, request):
        """Свободные номера на дату (?on=YYYY-MM-DD)"""
        on = parse_date(request.query_params.get("on")) or date.today()
        busy_stays = Stay.objects.filter(
            check_in__lte=on
        ).filter(
            Q(check_out__isnull=True) | Q(check_out__gt=on)
        )
        busy = busy_stays.values_list("room_id", flat=True)
        free = Room.objects.exclude(id__in=busy)
        return response.Response({
            "date": on,
            "free_count": free.count(),
            "free_rooms": RoomSerializer(free, many=True).data
        })

    # Дополнительное действие: клиенты, проживавшие в номере за период
    # Используется для аналитики и отчетов по конкретному номеру
    @decorators.action(detail=True, methods=["get"], url_path="clients")
    def clients_in_period(self, request, pk=None):
        """Клиенты, проживавшие в номере за период ?start&end"""
        room = self.get_object()
        start = parse_date(request.query_params.get("start"))
        end = parse_date(request.query_params.get("end"))
        if not start or not end:
            return response.Response({"detail": "start и end обязательны"}, status=400)
        stays = Stay.objects.filter(room=room).filter(
            check_in__lte=end
        ).filter(
            Q(check_out__isnull=True) | Q(check_out__gte=start)
        )
        clients = Client.objects.filter(stays__in=stays.values_list('id', flat=True)).distinct()
        return response.Response(ClientListItemSerializer(clients, many=True).data)


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ КЛИЕНТОВ =====

# ViewSet для управления клиентами гостиницы
# Предоставляет полный CRUD функционал + аналитические действия
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Дополнительное действие: подсчет клиентов по городу
    # Используется для статистики и аналитики по географическому распределению
    @decorators.action(detail=False, methods=["get"], url_path="count-by-city")
    def count_by_city(self, request):
        city = request.query_params.get("city")
        if not city:
            return response.Response({"detail": "city обязателен"}, status=400)
        count = Client.objects.filter(city__iexact=city).count()
        return response.Response({"city": city, "count": count})

    # Дополнительное действие: кто убирал номер клиента в определенный день недели
    # Используется для определения ответственного сотрудника за уборку
    @decorators.action(detail=True, methods=["get"], url_path="cleaner")
    def cleaner_on_weekday(self, request, pk=None):
        """Кто убирал номер клиента в день недели (?weekday=1..7)"""
        client = self.get_object()
        weekday = int(request.query_params.get("weekday", 0))
        if weekday not in range(1, 8):
            return response.Response({"detail": "weekday 1..7"}, status=400)
        stay = client.stays.order_by("-check_in").first()
        if not stay:
            return response.Response({"detail": "Нет данных о проживании"}, status=404)
        cleaners = Employee.objects.filter(
            schedules__weekday=weekday,
            schedules__floor=stay.room.floor,
            is_active=True,
        ).distinct()
        return response.Response(EmployeeSerializer(cleaners, many=True).data)

    # Дополнительное действие: клиенты, проживавшие одновременно с указанным клиентом
    # Используется для поиска потенциальных контактов и аналитики пересечений
    @decorators.action(detail=True, methods=["get"], url_path="co-stayers")
    def co_stayers(self, request, pk=None):
        """Клиенты, проживавшие в те же дни, что и указанный клиент"""
        client = self.get_object()
        start = parse_date(request.query_params.get("start"))
        end = parse_date(request.query_params.get("end"))
        if not start or not end:
            return response.Response({"detail": "start и end обязательны"}, status=400)
        overlapping = Stay.objects.filter(
            check_in__lte=end
        ).filter(
            Q(check_out__isnull=True) | Q(check_out__gte=start)
        ).exclude(client=client)
        clients = Client.objects.filter(stays__in=overlapping.values_list('id', flat=True)).distinct()
        return response.Response(ClientListItemSerializer(clients, many=True).data)


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ ПРОЖИВАНИЙ =====

# ViewSet для управления проживаниями клиентов
# Предоставляет полный CRUD функционал для регистрации заселений и выселений
class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.select_related("client", "room")
    serializer_class = StaySerializer
    permission_classes = [IsAdminOrReadOnly]


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ СОТРУДНИКОВ =====

# ViewSet для управления сотрудниками гостиницы
# Предоставляет полный CRUD функционал + действия для приема/увольнения
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Дополнительное действие: увольнение сотрудника
    # Устанавливает статус is_active = False
    @decorators.action(detail=True, methods=["post"], url_path="fire")
    def fire(self, request, pk=None):
        emp = self.get_object()
        emp.is_active = False
        emp.save(update_fields=["is_active"])
        return response.Response(EmployeeSerializer(emp).data)

    # Дополнительное действие: прием сотрудника на работу
    # Устанавливает статус is_active = True
    @decorators.action(detail=True, methods=["post"], url_path="hire")
    def hire(self, request, pk=None):
        emp = self.get_object()
        emp.is_active = True
        emp.save(update_fields=["is_active"])
        return response.Response(EmployeeSerializer(emp).data)


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ РАСПИСАНИЯ СОТРУДНИКОВ =====

# ViewSet для управления расписанием работы сотрудников
# Предоставляет полный CRUD функционал для назначения сотрудников на этажи по дням недели
class EmployeeScheduleViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSchedule.objects.select_related("employee")
    serializer_class = EmployeeScheduleSerializer
    permission_classes = [IsAdminOrReadOnly]


# ===== ПРЕДСТАВЛЕНИЯ ДЛЯ ОТЧЕТОВ =====

# API View для генерации квартальных отчетов
# Предоставляет детальную аналитику по доходам, клиентам и загруженности номеров
class QuarterReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Отчёт по кварталу ?quarter=1..4"""
        q = int(request.query_params.get("quarter", 1))
        year = date.today().year
        if q not in (1, 2, 3, 4):
            return response.Response({"detail": "quarter 1..4"}, status=400)

        q_start_month = (q - 1) * 3 + 1
        start = date(year, q_start_month, 1)
        end = date(year + (q == 4), (q_start_month + 3 - 1) % 12 + 1, 1) - timedelta(days=1)

        # Кол-во клиентов по каждому номеру
        room_client_counts = []
        for room in Room.objects.all():
            c = Client.objects.filter(
                stays__room=room,
                stays__check_in__lte=end,
                stays__check_out__gte=start
            ).distinct().count()
            room_client_counts.append({"room": room.number, "clients": c})

        # Количество номеров на этажах
        floors = Room.objects.values("floor").annotate(count=Count("id")).order_by("floor")

        # Доход
        def overlap_nights(s: Stay, start, end):
            s_end = s.check_out or end
            a = max(s.check_in, start)
            b = min(s_end, end)
            return max(0, (b - a).days)

        total_income = Decimal("0")
        room_income = []
        for room in Room.objects.all():
            stays = Stay.objects.filter(
                room=room, check_in__lte=end
            ).filter(
                Q(check_out__isnull=True) | Q(check_out__gte=start)
            )
            income = sum(Decimal(str(room.daily_rate)) * overlap_nights(s, start, end) for s in stays)
            total_income += income
            room_income.append({"room": room.number, "income": income})

        return response.Response({
            "period": {"start": start, "end": end},
            "clients_per_room": room_client_counts,
            "rooms_per_floor": list(floors),
            "income_per_room": room_income,
            "total_income": total_income,
        })
