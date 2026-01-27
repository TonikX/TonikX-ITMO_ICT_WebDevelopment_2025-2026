from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Floor, Room, Guest, LivingRecord, Staff, CleaningSchedule, CleaningRecord
from .serializers import (FloorSerializer, RoomSerializer, GuestSerializer, LivingRecordSerializer, 
                          StaffSerializer, CleaningScheduleSerializer, FloorFullSerializer, RoomFullSerializer,
                          GuestFullSerializer, StaffFullSerializer, CleaningScheduleSimpleSerializer, 
                          LivingRecordSimpleSerializer, CleaningRecordSerializer, CleaningRecordSimpleSerializer)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date
from django.db.models import Count, Q
from django.utils.decorators import method_decorator

def tagged_viewset(tag_name):
    def wrapper(cls):
        actions = ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']
        for action in actions:
            if hasattr(cls, action):
                decorator = swagger_auto_schema(tags=[tag_name])
                setattr(cls, action, method_decorator(decorator, name=action)(getattr(cls, action)))
        return cls
    return wrapper

@tagged_viewset('Floor')
class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FloorFullSerializer
        return FloorSerializer

@tagged_viewset('Room')
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RoomFullSerializer
        return RoomSerializer
    
    @swagger_auto_schema(
        operation_description="Кол-во свободных номеров",
        responses={200: openapi.Response(
            description="Кол-во свободных номеров",
            schema=openapi.Schema(type=openapi.TYPE_INTEGER)
        )},
        tags=['dop_requests']
    )
    @action(detail=False, methods=['get'])
    def count_not_occupied(self, request):
        today = date.today()
        n_free_rooms = Room.objects.exclude(
            Q(living_records__end_date__gte=today) | Q(living_records__end_date__isnull=True),
            living_records__start_date__lte=today).count()
        return Response(n_free_rooms)

@tagged_viewset('Guest')
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GuestFullSerializer
        return GuestSerializer
    
    @swagger_auto_schema(
        operation_description="Гости по городу",
        manual_parameters=[
            openapi.Parameter('city', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: openapi.Response(
            description="Кол-во гостей из города",
            schema=openapi.Schema(type=openapi.TYPE_INTEGER)
        )},
        tags=['dop_requests']
    )
    @action(detail=False, methods=['get'])
    def count_by_city(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({"error": "Укажите параметр city"}, status=status.HTTP_400_BAD_REQUEST)
        n_guests = Guest.objects.filter(city=city).count()
        return Response(n_guests)
    
    @swagger_auto_schema(
        operation_description="Гости за период по номеру",
        manual_parameters=[
            openapi.Parameter('room_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: GuestSerializer(many=True)},
        tags=['dop_requests']
    )
    @action(detail=False, methods=['get'])
    def by_room_period(self, request):
        room_id = request.query_params.get('room_id')
        start = request.query_params.get('start_date')
        end = request.query_params.get('end_date')
        records = LivingRecord.objects.filter(
            Q(end_date__gte=start) | Q(end_date__isnull=True),
            room_id=room_id,
            start_date__lte=end,
        ).select_related('guest')

        guests = [record.guest for record in records]
        return Response(GuestSerializer(guests, many=True).data)
    
    @swagger_auto_schema(
        operation_description="Гости в тот же период по гостю",
        manual_parameters=[
            openapi.Parameter('guest_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: GuestSerializer(many=True)},
        tags=['dop_requests']
    )
    @action(detail=False, methods=['get'])
    def by_guest_period(self, request):
        guest_id = request.query_params.get('guest_id')
        start = request.query_params.get('start_date')
        end = request.query_params.get('end_date')
        guest_record = LivingRecord.objects.filter(
            guest_id=guest_id,
            start_date__gte=start,
            end_date__lte=end
            ).first()
        
        start = max(str(guest_record.start_date), start)
        end = min(str(guest_record.end_date) or end, end)
        guests = Guest.objects.filter(
            living_records__start_date__lte=end,
            living_records__end_date__gte=start
        ).exclude(pk=guest_id).distinct()

        return Response(GuestSerializer(guests, many=True).data)

@tagged_viewset('LivingRecord')
class LivingRecordViewSet(viewsets.ModelViewSet):
    queryset = LivingRecord.objects.all()
    serializer_class = LivingRecordSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LivingRecordSimpleSerializer
        return LivingRecordSerializer
    
    @swagger_auto_schema(
        operation_description="Проживания сейчас",
        responses={200: LivingRecordSerializer},
        tags=['dop_requests']
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        today_date = date.today()
        active_living_records = LivingRecord.objects.filter(
            Q(end_date__gte=today_date) | Q(end_date__isnull=True),
            start_date__lte=today_date
        )
        return Response(LivingRecordSerializer(active_living_records, many=True).data)

@tagged_viewset('Staff')
class StaffViewSet(viewsets.ModelViewSet):
    queryset= Staff.objects.all()
    serializer_class = StaffSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StaffFullSerializer
        return StaffSerializer
    
    @swagger_auto_schema(
        operation_description="Сотрудник, который убирал номер клиента в заданый день",
        manual_parameters=[
            openapi.Parameter('guest_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: StaffSerializer(many=True)},
        tags=['dop_requests']
    )
    @action(detail=False, methods=['get'])
    def by_guest_day(self, request):
        guest_id = request.query_params.get('guest_id')
        cleaning_date = request.query_params.get('date')
        if not guest_id or not date:
            return Response({"error": "не указаны нужные параметры"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            living_record = LivingRecord.objects.filter(
                Q(end_date__gte=cleaning_date) | Q(end_date__isnull=True),
                guest_id=guest_id,
                start_date__lte=cleaning_date,
                ).first()
            if not living_record:
                return Response({"error": "Данный гость не проживал в данную дату"}, status=status.HTTP_400_BAD_REQUEST)
            floor = living_record.room.floor
            staff = CleaningRecord.objects.get(floor=floor, cleaning_date=cleaning_date).staff
            return Response(StaffSerializer(staff).data)
        except:
            return Response({"error": "Ошибка при обработке"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@tagged_viewset('CleaningSchedule')
class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CleaningScheduleSimpleSerializer
        return CleaningScheduleSerializer

@tagged_viewset('CleaningRecord')
class CleaningRecordViewSet(viewsets.ModelViewSet):
    queryset = CleaningRecord.objects.all()
    serializer_class = CleaningRecordSerializer

    def get_serializer_class(self):
        print(self.queryset)
        if self.action in ['create', 'update', 'partial_update']:
            return CleaningRecordSimpleSerializer
        return CleaningRecordSerializer

@swagger_auto_schema(
    method='get',
    operation_description="Получить отчёт за квартал",
    manual_parameters=[
        openapi.Parameter('quarter', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)
    ],
    responses={200: "Отчёт за квартал"},
    tags=['dop_requests']
)
@api_view(['GET'])
def hotel_quarterly_report(request):
    quarter = request.query_params.get('quarter')
    year_now = date.today().year
    quarters = {
        1: (date(year_now, 1, 1), date(year_now, 3, 31)),
        2: (date(year_now, 4, 1), date(year_now, 6, 30)),
        3: (date(year_now, 7, 1), date(year_now, 9, 30)),
        4: (date(year_now, 10, 1), date(year_now, 12, 31)),
    }
    start_date, end_date = quarters[int(quarter)]
    rooms = Room.objects.all()
    room_report = []
    income = 0
    for room in rooms:
        living_records = LivingRecord.objects.filter(
                room=room,
                start_date__lte=end_date,
                end_date__gte=start_date
            )
        guest_count = living_records.count()
        income_room = 0
        for record in living_records:
            start = max(start_date, record.start_date)
            end = min(end_date, record.end_date or date.today())
            if end < start:
                continue
            income_room += float(room.price) * (end - start).days + 1
        room_report.append({
            'room_id': room.id,
            'guests': guest_count,
            'income': str(round(income_room, 2))
        })
        income += income_room
    floor_count = Floor.objects.annotate(room_count=Count('rooms'))
    floor_report = {floor.id: floor.room_count for floor in floor_count}
    return Response({
        "income":  str(round(income, 2)),
        "room_report": room_report,
        "floor_report": floor_report
    })