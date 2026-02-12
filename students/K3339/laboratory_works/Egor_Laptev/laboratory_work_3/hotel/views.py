from datetime import date

from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    @action(detail=False, methods=["get"])
    def stats(self, request):
        data = (
            RoomType.objects.annotate(rooms_count=Count("rooms"))
            .values("id", "name", "capacity", "price_per_day", "rooms_count")
            .order_by("id")
        )
        return Response(data)


class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    @action(detail=False, methods=["get"])
    def stats(self, request):
        data = (
            Floor.objects.annotate(
                rooms_count=Count("rooms", distinct=True),
                cleaning_count=Count("cleaning_schedules", distinct=True),
            )
            .values("id", "number", "rooms_count", "cleaning_count")
            .order_by("number")
        )
        return Response(data)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer

    @action(detail=False, methods=["get"])
    def summary(self, request):
        today = request.query_params.get("date")
        summary_date = None
        if today:
            try:
                summary_date = date.fromisoformat(today)
            except ValueError:
                return Response({"detail": "date must be YYYY-MM-DD"}, status=400)
        else:
            summary_date = date.today()

        active_q = Q(check_in__lte=summary_date, check_out__gt=summary_date)

        total_stays = Stay.objects.count()
        active = Stay.objects.filter(active_q).count()
        upcoming = Stay.objects.filter(check_in__gt=summary_date).count()

        data = {
            "date": summary_date.isoformat(),
            "total_stays": total_stays,
            "active_now": active,
            "upcoming": upcoming,
            "active_rooms": Stay.objects.filter(active_q).aggregate(
                active_rooms=Count("room", distinct=True)
            )["active_rooms"],
        }
        return Response(data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
