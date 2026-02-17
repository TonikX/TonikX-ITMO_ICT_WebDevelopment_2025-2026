from django.db.models import Sum, Count, Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *

# Справочники
class RoomTypeList(generics.ListCreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

# Основные
class FloorList(generics.ListCreateAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    
class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'floor__number', 'room_type__max_guests']

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GuestList(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city__name', 'last_name']

class GuestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# Операции
class BookingList(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['guest__last_name', 'room__number', 'is_active', 'check_in']

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class CleaningScheduleList(generics.ListCreateAPIView):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer

class CleaningScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer

class HotelAnalyticsView(APIView):
    """
    Эндпоинт для выполнения специфических информационных запросов и генерации
    отчетов о работе гостиницы.
    """
    def get(self, request):
        query_type = request.query_params.get('type')

        # --- 1. КВАРТАЛЬНЫЙ ОТЧЕТ ---
        if query_type == 'quarterly_report':
            quarter = request.query_params.get('quarter') # 1, 2, 3 или 4
            year = request.query_params.get('year', datetime.date.today().year)
            
            if not quarter:
                return Response({"error": "Укажите номер квартала (1-4)"}, status=400)
            
            try:
                year = int(year)
                # Определение временных границ кварталов
                q_dates = {
                    '1': ((1, 1), (3, 31)),
                    '2': ((4, 1), (6, 30)),
                    '3': ((7, 1), (9, 30)),
                    '4': ((10, 1), (12, 31)),
                }
                
                (start_m, start_d), (end_m, end_d) = q_dates.get(quarter)
                start_date = datetime.date(year, start_m, start_d)
                end_date = datetime.date(year, end_m, end_d)

                # А) Число клиентов и доход за период в каждом номере
                # Используем фильтрованные агрегации (Conditional Aggregation)
                room_stats = Room.objects.annotate(
                    clients_count=Count('bookings', filter=Q(bookings__check_in__range=(start_date, end_date))),
                    income=Sum('bookings__total_cost', filter=Q(bookings__check_in__range=(start_date, end_date)))
                ).values('number', 'clients_count', 'income')

                # Б) Количество номеров на каждом этаже
                floor_stats = Floor.objects.annotate(
                    rooms_count=Count('rooms')
                ).values('number', 'rooms_count')

                # В) Суммарный доход по всей гостинице
                total_income = Booking.objects.filter(
                    check_in__range=(start_date, end_date)
                ).aggregate(total=Sum('total_cost'))['total'] or 0

                return Response({
                    "period": f"Квартал {quarter}, {year}",
                    "rooms_efficiency": list(room_stats),
                    "floors_structure": list(floor_stats),
                    "total_hotel_income": total_income
                })
            except (ValueError, TypeError, KeyError):
                return Response({"error": "Некорректные параметры квартала или года"}, status=400)

        # --- 2. О клиентах, проживавших в заданном номере в заданный период ---
        elif query_type == 'clients_in_room':
            room_num = request.query_params.get('room')
            start = request.query_params.get('start')
            end = request.query_params.get('end')
            bookings = Booking.objects.filter(
                room__number=room_num,
                check_in__lte=end,
                check_out__gte=start
            )
            data = [{"fio": f"{b.guest.last_name} {b.guest.first_name}", "from": b.check_in, "to": b.check_out} for b in bookings]
            return Response(data)

        # --- 3. О количестве клиентов из заданного города ---
        elif query_type == 'clients_by_city':
            city_id = request.query_params.get('city_id')
            count = Guest.objects.filter(city_id=city_id).count()
            return Response({"count": count})

        # --- 4. Кто убирал номер указанного клиента в заданный день недели ---
        elif query_type == 'cleaner_info':
            guest_id = request.query_params.get('guest_id')
            day = request.query_params.get('day') # 'mon', 'tue'...
            # Находим активную бронь гостя
            booking = Booking.objects.filter(guest_id=guest_id, is_active=True).first()
            if not booking:
                return Response({"error": "Активное проживание не найдено"}, status=404)
            
            floor = booking.room.floor
            schedules = CleaningSchedule.objects.filter(floor=floor, day_of_week=day)
            cleaners = [f"{s.employee.last_name} {s.employee.first_name}" for s in schedules]
            return Response({"cleaners": cleaners, "floor": floor.number, "room": booking.room.number})

        # --- 5. Сколько в гостинице свободных номеров ---
        elif query_type == 'free_rooms':
            count = Room.objects.filter(status='free').count()
            return Response({"free_rooms_count": count})

        # --- 6. Список "соседей" (пересечение дат проживания) ---
        elif query_type == 'overlapping_guests':
            target_guest_id = request.query_params.get('guest_id')
            # Находим последнюю или текущую бронь целевого клиента
            target_b = Booking.objects.filter(guest_id=target_guest_id).order_by('-check_in').first()
            if not target_b:
                return Response({"error": "Клиент не найден в базе бронирований"}, status=404)
            
            # Ищем пересечения по датам
            others = Booking.objects.filter(
                check_in__lt=target_b.check_out if target_b.check_out else datetime.date.max,
                check_out__gt=target_b.check_in
            ).exclude(guest_id=target_guest_id)

            data = [{
                "fio": f"{b.guest.last_name} {b.guest.first_name}",
                "city": b.guest.city.name,
                "room": b.room.number,
                "period": f"{b.check_in} - {b.check_out}"
            } for b in others]
            return Response(data)

        return Response({"error": "Неверный тип запроса или отсутствуют параметры"}, status=400)