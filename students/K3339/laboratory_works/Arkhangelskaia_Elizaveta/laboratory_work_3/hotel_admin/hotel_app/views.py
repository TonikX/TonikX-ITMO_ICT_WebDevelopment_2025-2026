from django.db.models.functions import TruncDate
from rest_framework import generics
from datetime import date
from .serializers import *
from django.db.models.functions import Concat
from django.db.models import Value, CharField
from django.db.models import Count, Sum, F
from django.db.models.functions import Greatest, Least, Extract
from rest_framework.response import Response


class ResidentsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Residents.objects.all()
    serializer_class = ResidentsSerializer


class ResidentsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Residents.objects.all()
    serializer_class = ResidentsSerializer


class RoomsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializer


class RoomsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializer


class RoomTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class ReservationsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class WorkersListCreateAPIView(generics.ListCreateAPIView):
    queryset = Workers.objects.all()
    serializer_class = WorkersSerializer


class WorkersRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workers.objects.all()
    serializer_class = WorkersSerializer


class CleaningInformationListCreateAPIView(generics.ListCreateAPIView):
    queryset = CleaningInformation.objects.all()
    serializer_class = CleaningInformationSerializer


class CleaningInformationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CleaningInformation.objects.all()
    serializer_class = CleaningInformationSerializer


class CleaningListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cleaning.objects.all()
    serializer_class = CleaningSerializer


class CleaningRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cleaning.objects.all()
    serializer_class = CleaningSerializer


class ResidentsAPIView(generics.ListAPIView):
    serializer_class = ResidentsSerializer


    def get_queryset(self):
        queryset = Residents.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        room_number = self.request.query_params.get('room_number')
        try:
            room = Rooms.objects.get(room_number=room_number)
        except Rooms.DoesNotExist:
            return Residents.objects.none()

        if not start_date or not end_date:
            reservations = Reservation.objects.filter(
                rooms=room
            )
        else:
            reservations = Reservation.objects.filter(
                start_date__lte=end_date,
                end_date__gte=start_date,
                rooms=room
            )

        queryset = queryset.filter(reservations__in=reservations).distinct()

        return queryset


class CityAPIView(generics.ListAPIView):
    serializer_class = ResidentsSerializer

    def get_queryset(self):
        city = self.request.query_params.get('city')
        queryset = Residents.objects.filter(city=city)
        return queryset


class AvailableRoomsAPIView(generics.ListAPIView):
    serializer_class = RoomsSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        busy_rooms = []
        if start_date and end_date:
            busy_rooms = Rooms.objects.filter(
                reservations__start_date__lte=end_date,
                reservations__end_date__gte=start_date
            )

        free_rooms = Rooms.objects.exclude(id__in=busy_rooms)
        return free_rooms


class ClientsAPIView(generics.ListAPIView):
    serializer_class = ResidentsSerializer


    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        id_client = self.request.query_params.get('id_client')
        if not (start_date and end_date and id_client):
            return Residents.objects.none()

        try:
            Residents.objects.get(pk=id_client)
        except Rooms.DoesNotExist:
            return Residents.objects.none()

        queryset = Residents.objects.filter(
            reservations__start_date__lte=end_date,
            reservations__end_date__gte=start_date
        ).exclude(pk=id_client).distinct()

        return queryset


class CleaningStaffAPIView(generics.ListAPIView):
    serializer_class = RequestCleaningSerializer


    def get_queryset(self):
        id_client = self.request.query_params.get('id_client')
        week_day = self.request.query_params.get('week_day')
        week_days = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

        if week_day not in week_days:
            return Workers.objects.none()

        try:
            Residents.objects.get(pk=id_client)
        except Rooms.DoesNotExist:
            return Residents.objects.none()

        django_weekday = ((week_days.index(week_day) + 1) % 7) + 1

        cleanings = (
            Cleaning.objects
            .annotate(
                cleaning_day=TruncDate("cleaning_date"),
                worker_full_name=Concat(
                    F('worker__surname'), Value(' '),
                    F('worker__name'), Value(' '),
                    F('worker__patronymic'),
                    output_field=CharField()
                )
            )
            .filter(
                cleaning_date__week_day=django_weekday,  # фильтр по дню недели
                room__reservations__residents__id=id_client,
                room__reservations__start_date__lte=F("cleaning_day"),
                room__reservations__end_date__gte=F("cleaning_day"),
            )
            .select_related("worker", "room")
            .values(
                "cleaning_day",
                "room__room_number",
                "worker_full_name"
            )
            .distinct()
        )

        return cleanings


class ReportAPIView(generics.GenericAPIView):
    pagination_class = None

    def get(self, request, *args, **kwargs):
        year = self.request.query_params.get('year')
        quarter = self.request.query_params.get('quarter')
        dates = {
            '1': ('01-01', '03-31'),
            '2': ('04-01', '06-30'),
            '3': ('07-01', '10-31'),
            '4': ('11-01', '12-31')
        }
        start_date = date.fromisoformat(f"{year}-{dates[quarter][0]}")
        end_date = date.fromisoformat(f"{year}-{dates[quarter][1]}")

        clients_per_room = (
            Reservation.objects
            .filter(start_date__lt=end_date, end_date__gt=start_date)
            .values(room_number=F("rooms__room_number"))
            .annotate(clients_count=Count("residents", distinct=True))
        )

        # Количество номеров на каждом этаже
        rooms_per_floor = (
            Rooms.objects
            .values("floor")
            .annotate(rooms_count=Count("id"))
        )

        # Доход по каждому номеру
        income_per_room = (
            Reservation.objects
            .filter(start_date__lt=end_date, end_date__gt=start_date)
            .annotate(
                actual_start=Greatest(F("start_date"), Value(start_date)),
                actual_end=Least(F("end_date"), Value(end_date)),
                days=Extract(F("actual_end") - F("actual_start"), 'day') + 1,  # количество дней
                income=F("days") * F("rooms__id_room_type__price")
            )
            .values(room_number=F("rooms__room_number"))
            .annotate(total_income=Sum("income"))
        )

        # Суммарный доход по гостинице
        total_income = income_per_room.aggregate(
            total=Sum("total_income")
        )["total"]

        return Response({
            "year": year,
            "quarter": quarter,
            "clients_per_room": clients_per_room,
            "rooms_per_floor": rooms_per_floor,
            "income_per_room": income_per_room,
            "total_hotel_income": total_income
        })
        
