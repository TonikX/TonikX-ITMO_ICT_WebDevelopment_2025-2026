from rest_framework import viewsets
from .models import Floor, Room, Client, StayRecord, Employee, CleaningSchedule, CleaningRecord
from .serializers import (
    FloorSerializer, RoomSerializer, ClientSerializer,
    StayRecordSerializer, EmployeeSerializer,
    CleaningScheduleSerializer, CleaningRecordSerializer, FloorDetailSerializer
)
from django.db.models import Count
from rest_framework.decorators import action, api_view
from rest_framework.response import Response


class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FloorDetailSerializer
        return FloorSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    def usage_stats(self, request):
        rooms = Room.objects.annotate(
            stays_count=Count('stay_records')
        ).values(
            'id', 'number', 'room_type', 'price_per_day', 'stays_count'
        )
        return Response(rooms)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False, methods=['get'])
    def activity_stats(self, request):
        clients = Client.objects.annotate(
            stays_count=Count('stay_records')
        ).values(
            'id', 'first_name', 'last_name', 'city', 'stays_count'
        ).order_by('-stays_count')

        return Response(clients)



class StayRecordViewSet(viewsets.ModelViewSet):
    queryset = StayRecord.objects.all()
    serializer_class = StayRecordSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer


class CleaningRecordViewSet(viewsets.ModelViewSet):
    queryset = CleaningRecord.objects.all()
    serializer_class = CleaningRecordSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, F
from datetime import date

from .models import Room, StayRecord


class HotelReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            quarter = int(request.GET.get("quarter"))
            year = int(request.GET.get("year"))
        except (TypeError, ValueError):
            return Response({"error": "quarter и year обязательны"}, status=400)

        quarter_dates = {
            1: (date(year, 1, 1), date(year, 3, 31)),
            2: (date(year, 4, 1), date(year, 6, 30)),
            3: (date(year, 7, 1), date(year, 9, 30)),
            4: (date(year, 10, 1), date(year, 12, 31)),
        }

        if quarter not in quarter_dates:
            return Response({"error": "Некорректный квартал"}, status=400)

        start, end = quarter_dates[quarter]

        stays = StayRecord.objects.select_related("room", "client").filter(
            check_in_date__lte=end,
            check_out_date__gte=start
        )

        # ---------- доход по комнатам ----------
        income_per_room = {}
        total_income = 0

        for stay in stays:
            days = (stay.check_out_date - stay.check_in_date).days
            days = max(days, 1)  # защита от 0 дней
            income = days * stay.room.price_per_day

            room_number = stay.room.number
            income_per_room[room_number] = income_per_room.get(room_number, 0) + income
            total_income += income

        # ---------- клиенты по комнатам ----------
        clients_in_rooms = (
            stays
            .values("room__number")
            .annotate(client_count=Count("client", distinct=True))
        )

        clients_per_room = {
            item["room__number"]: item["client_count"]
            for item in clients_in_rooms
        }

        # ---------- комнаты по этажам ----------
        rooms_per_floor = (
            Room.objects
            .values("floor__number")
            .annotate(room_count=Count("id"))
        )

        return Response({
            "income_per_room": income_per_room,
            "clients_in_rooms": clients_per_room,
            "rooms_per_floor": list(rooms_per_floor),
            "total_income": total_income,
        })