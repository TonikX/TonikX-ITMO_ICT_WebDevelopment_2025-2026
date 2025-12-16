from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Count
from django.utils.dateparse import parse_date
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import models
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from .models import Room, Client, Employee, CleaningSchedule, Stay
from .serializers import (
    RoomSerializer,
    ClientSerializer,
    EmployeeSerializer,
    CleaningScheduleSerializer,
    StaySerializer,
    ClientWithCitySerializer,
    QuarterReportSerializer,
    CheckInActionSerializer,
    CheckInResultSerializer,
    HireEmployeeSerializer,
    HireEmployeeResultSerializer,
    RoomWithClientsSerializer,
    ClientWithRoomsSerializer,
)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'floor', 'weekday']


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['room', 'client', 'check_in', 'check_out']
    ordering_fields = ['check_in', 'check_out']
    ordering = ['-check_in']

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        today = date.today()

        if status_param == 'current_and_future':
            return queryset.filter(
                models.Q(check_out__isnull=True) | models.Q(check_out__gte=today)
            )

        if status_param == 'active':
            return queryset.filter(check_in__lte=today).filter(
                models.Q(check_out__isnull=True) | models.Q(check_out__gte=today)
            )
        elif status_param == 'future':
            return queryset.filter(check_in__gt=today)
        elif status_param == 'history':
            return queryset.filter(check_out__lt=today)

        return queryset

class WhoCleanedRoomView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        room_number = request.query_params.get("room_number")
        date_str = request.query_params.get("date")

        if not room_number or not date_str:
            return Response({"detail": "Нужны room_number и date (YYYY-MM-DD)"}, status=400)

        try:
            target_date = parse_date(date_str)
            weekday = target_date.weekday()

            room = Room.objects.get(number=room_number)

            schedule = CleaningSchedule.objects.filter(
                floor=room.floor,
                weekday=weekday,
                employee__is_active=True
            ).select_related('employee').first()

            if not schedule:
                return Response({"detail": "На этот день/этаж уборщик не назначен"}, status=404)

            return Response(EmployeeSerializer(schedule.employee).data)

        except Room.DoesNotExist:
            return Response({"detail": "Комната не найдена"}, status=404)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

class ClientsInRoomView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'room_number',
                openapi.IN_QUERY,
                description='Номер комнаты (например, 101)',
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'start',
                openapi.IN_QUERY,
                description='Дата начала периода (YYYY-MM-DD)',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True,
            ),
            openapi.Parameter(
                'end',
                openapi.IN_QUERY,
                description='Дата конца периода (YYYY-MM-DD)',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True,
            ),
        ],
        responses={200: ClientWithCitySerializer(many=True)},
    )
    def get(self, request):
        room_number = request.query_params.get("room_number")
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if not (room_number and start and end):
            return Response(
                {"detail": "Нужно передать room_number, start, end (YYYY-MM-DD)"},
                status=400,
            )

        start_date = parse_date(start)
        end_date = parse_date(end)

        stays = Stay.objects.filter(
            room__number=room_number,
            check_in__lte=end_date,
        ).filter(
            models.Q(check_out__isnull=True) | models.Q(check_out__gte=start_date)
        )

        clients = Client.objects.filter(stays__in=stays).distinct()
        serializer = ClientWithCitySerializer(clients, many=True)
        return Response(serializer.data)


class ClientsFromCityCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'city',
                openapi.IN_QUERY,
                description='Город клиента (например, "Санкт-Петербург")',
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'city': openapi.Schema(type=openapi.TYPE_STRING),
                    'clients_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                },
            )
        },
    )
    def get(self, request):
        city = request.query_params.get("city")
        if not city:
            return Response({"detail": "Передайте параметр city"}, status=400)

        count = Client.objects.filter(city__iexact=city).count()
        return Response({"city": city, "clients_count": count})


class CleanerForClientView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'client_id',
                openapi.IN_QUERY,
                description='ID клиента',
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'weekday',
                openapi.IN_QUERY,
                description='День недели: 0–понедельник, ..., 6–воскресенье',
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={200: EmployeeSerializer()},
    )
    def get(self, request):
        client_id = request.query_params.get("client_id")
        weekday = request.query_params.get("weekday")

        if client_id is None or weekday is None:
            return Response(
                {"detail": "Нужно передать client_id и weekday (0-6)"},
                status=400,
            )

        weekday = int(weekday)

        stay = (
            Stay.objects.filter(client_id=client_id)
            .order_by("-check_in")
            .first()
        )
        if not stay:
            return Response({"detail": "У клиента нет заселений"}, status=404)

        floor = stay.room.floor
        schedule = CleaningSchedule.objects.filter(
            floor=floor, weekday=weekday
        ).select_related("employee").first()

        if not schedule:
            return Response(
                {"detail": "Для этого этажа/дня недели расписание не найдено"},
                status=404,
            )

        serializer = EmployeeSerializer(schedule.employee)
        return Response(serializer.data)


class FreeRoomsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('check_in', openapi.IN_QUERY, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=True),
            openapi.Parameter('check_out', openapi.IN_QUERY, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=True),
        ],
    )
    def get(self, request):
        check_in_str = request.query_params.get("check_in")
        check_out_str = request.query_params.get("check_out")

        if not check_in_str or not check_out_str:
            return Response({"detail": "Нужны check_in и check_out"}, status=400)

        start = parse_date(check_in_str)
        end = parse_date(check_out_str)

        if not start or not end:
            return Response({"detail": "Некорректный формат дат"}, status=400)

        occupied_rooms_ids = Stay.objects.filter(
            check_in__lt=end
        ).filter(
            models.Q(check_out__isnull=True) | models.Q(check_out__gt=start)
        ).values_list('room_id', flat=True)

        free_rooms = Room.objects.exclude(id__in=occupied_rooms_ids)
        serializer = RoomSerializer(free_rooms, many=True)

        return Response(serializer.data)

class ClientsSameDaysView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'client_id',
                openapi.IN_QUERY,
                description='ID клиента, с которым сравниваем',
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'start',
                openapi.IN_QUERY,
                description='Дата начала периода (YYYY-MM-DD)',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True,
            ),
            openapi.Parameter(
                'end',
                openapi.IN_QUERY,
                description='Дата конца периода (YYYY-MM-DD)',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True,
            ),
        ],
        responses={200: ClientWithCitySerializer(many=True)},
    )
    def get(self, request):
        client_id = request.query_params.get("client_id")
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if not (client_id and start and end):
            return Response(
                {"detail": "Нужно передать client_id, start и end"},
                status=400,
            )

        start_date = parse_date(start)
        end_date = parse_date(end)

        target_stays = Stay.objects.filter(
            client_id=client_id,
            check_in__lte=end_date,
        ).filter(
            models.Q(check_out__isnull=True) | models.Q(check_out__gte=start_date)
        )

        if not target_stays.exists():
            return Response({"detail": "У клиента нет заселений в этот период"}, status=404)

        other_stays = Stay.objects.filter(
            check_in__lte=end_date,
        ).filter(
            models.Q(check_out__isnull=True) | models.Q(check_out__gte=start_date)
        ).exclude(client_id=client_id)

        def overlaps(a_start, a_end, b_start, b_end):
            if a_end is None:
                a_end = end_date
            if b_end is None:
                b_end = end_date
            return a_start <= b_end and b_start <= a_end

        target_intervals = [
            (s.check_in, s.check_out) for s in target_stays
        ]

        client_ids = set()
        for s in other_stays:
            for ti_start, ti_end in target_intervals:
                if overlaps(ti_start, ti_end, s.check_in, s.check_out):
                    client_ids.add(s.client_id)
                    break

        clients = Client.objects.filter(id__in=client_ids)
        serializer = ClientWithCitySerializer(clients, many=True)
        return Response(serializer.data)


class QuarterReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_quarter_dates(self, year: int, quarter: int):
        if quarter == 1:
            return date(year, 1, 1), date(year, 3, 31)
        if quarter == 2:
            return date(year, 4, 1), date(year, 6, 30)
        if quarter == 3:
            return date(year, 7, 1), date(year, 9, 30)
        if quarter == 4:
            return date(year, 10, 1), date(year, 12, 31)
        raise ValueError("quarter must be 1..4")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'year',
                openapi.IN_QUERY,
                description='Год отчёта (по умолчанию текущий год)',
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                'quarter',
                openapi.IN_QUERY,
                description='Квартал: 1, 2, 3 или 4',
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={200: QuarterReportSerializer()},
    )
    def get(self, request):
        year = request.query_params.get("year")
        quarter = request.query_params.get("quarter")

        if not quarter:
            return Response({"detail": "Передайте quarter=1..4"}, status=400)

        quarter = int(quarter)
        if year:
            year = int(year)
        else:
            year = date.today().year

        start_q, end_q = self.get_quarter_dates(year, quarter)

        stays = Stay.objects.filter(
            check_in__lte=end_q,
        ).filter(
            models.Q(check_out__isnull=True) | models.Q(check_out__gte=start_q)
        ).select_related("room")

        per_room = {}
        for s in stays:
            room = s.room
            key = room.id
            s_start = max(s.check_in, start_q)
            s_end = s.check_out or end_q
            s_end = min(s_end, end_q)
            nights = max((s_end - s_start).days, 0)

            info = per_room.setdefault(
                key,
                {
                    "room": room,
                    "clients": set(),
                    "nights": 0,
                    "income": Decimal("0.00"),
                },
            )
            info["clients"].add(s.client_id)
            info["nights"] += nights
            info["income"] += room.daily_price * nights

        rooms_report = []
        total_income = Decimal("0.00")
        for info in per_room.values():
            rooms_report.append(
                {
                    "room_number": info["room"].number,
                    "clients_count": len(info["clients"]),
                    "income": info["income"],
                }
            )
            total_income += info["income"]

        rooms_per_floor = list(
            Room.objects.values("floor").annotate(count=Count("id"))
        )

        data = {
            "rooms": rooms_report,
            "rooms_per_floor": rooms_per_floor,
            "total_income": total_income,
        }

        serializer = QuarterReportSerializer(data)
        return Response(serializer.data)

class CheckInActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=CheckInActionSerializer,
        responses={201: CheckInResultSerializer()},
    )
    def post(self, request):
        serializer = CheckInActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        with transaction.atomic():
            client, created = Client.objects.get_or_create(
                passport_number=data["passport_number"],
                defaults={
                    "last_name": data["last_name"],
                    "first_name": data["first_name"],
                    "patronymic": data.get("patronymic", ""),
                    "city": data["city"],
                },
            )
            if not created:
                client.last_name = data["last_name"]
                client.first_name = data["first_name"]
                client.patronymic = data.get("patronymic", "")
                client.city = data["city"]
                client.save()

            try:
                room = Room.objects.get(number=data["room_number"])
            except Room.DoesNotExist:
                return Response(
                    {"detail": "Номер с таким номером комнаты не найден"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            check_in = data["check_in"]
            check_out = data.get("check_out")

            end_for_overlap = check_out or check_in

            overlaps = Stay.objects.filter(
                room=room,
                check_in__lt=end_for_overlap,
            ).filter(
                Q(check_out__isnull=True) | Q(check_out__gt=check_in)
            )

            if overlaps.exists():
                return Response(
                    {"detail": "Номер занят на выбранные даты"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            stay = Stay.objects.create(
                client=client,
                room=room,
                check_in=check_in,
                check_out=check_out,
            )

            if check_out:
                nights = max((check_out - check_in).days, 0)
                total_price = room.daily_price * nights
            else:
                total_price = Decimal("0.00")

        result = CheckInResultSerializer(
            {
                "client": client,
                "room": room,
                "stay": stay,
                "total_price": total_price,
            }
        )
        return Response(result.data, status=status.HTTP_201_CREATED)


class HireEmployeeActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=HireEmployeeSerializer,
        responses={201: HireEmployeeResultSerializer()},
    )
    def post(self, request):
        serializer = HireEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        with transaction.atomic():
            employee = Employee.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                patronymic=data.get("patronymic", ""),
                is_active=data.get("is_active", True),
            )

            created_schedules = []
            for item in data["schedules"]:
                schedule, _ = CleaningSchedule.objects.get_or_create(
                    employee=employee,
                    floor=item["floor"],
                    weekday=item["weekday"],
                )
                created_schedules.append(schedule)

        result = HireEmployeeResultSerializer(
            {"employee": employee, "schedules": created_schedules}
        )
        return Response(result.data, status=status.HTTP_201_CREATED)

class RoomsWithClientsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Список номеров с вложенным списком клиентов.",
        responses={200: RoomWithClientsSerializer(many=True)},
    )
    def get(self, request):
        rooms = Room.objects.prefetch_related("clients")
        serializer = RoomWithClientsSerializer(rooms, many=True)
        return Response(serializer.data)


class ClientsWithRoomsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Список клиентов с вложенным списком номеров.",
        responses={200: ClientWithRoomsSerializer(many=True)},
    )
    def get(self, request):
        clients = Client.objects.prefetch_related("rooms")
        serializer = ClientWithRoomsSerializer(clients, many=True)
        return Response(serializer.data)
