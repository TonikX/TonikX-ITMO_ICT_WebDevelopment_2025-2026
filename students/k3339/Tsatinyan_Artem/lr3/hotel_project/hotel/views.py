from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Count
from django.utils.dateparse import parse_date
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Room, Client, Employee, CleaningSchedule, Stay
from .serializers import (
    RoomSerializer,
    ClientSerializer,
    EmployeeSerializer,
    CleaningScheduleSerializer,
    StaySerializer,
    ClientWithCitySerializer,
    QuarterReportSerializer,
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


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer
    permission_classes = [permissions.IsAuthenticated]

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
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description='Дата, на которую ищем свободные номера (YYYY-MM-DD). '
                            'Если не указана — используется сегодняшняя.',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'date': openapi.Schema(type=openapi.TYPE_STRING),
                    'free_rooms': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT),
                    ),
                },
            )
        },
    )
    def get(self, request):
        date_str = request.query_params.get("date")
        if date_str:
            target_date = parse_date(date_str)
        else:
            target_date = date.today()

        occupied_rooms = Room.objects.filter(
            stays__check_in__lte=target_date
        ).filter(
            models.Q(stays__check_out__isnull=True)
            | models.Q(stays__check_out__gte=target_date)
        ).distinct()

        free_rooms = Room.objects.exclude(id__in=occupied_rooms)
        serializer = RoomSerializer(free_rooms, many=True)
        return Response(
            {"date": str(target_date), "free_rooms": serializer.data}
        )


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