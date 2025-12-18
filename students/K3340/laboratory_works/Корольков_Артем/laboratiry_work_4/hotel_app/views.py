from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from datetime import datetime, date
from .models import RoomType, Room, Client, Staff, CleaningSchedule, Stay
from .serializers import *


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    def available_rooms(self, request):
        """Количество свободных номеров в гостинице"""
        available_count = Room.objects.filter(is_available=True).count()
        return Response({'available_rooms': available_count})

    @action(detail=False, methods=['get'])
    def rooms_by_floor(self, request):
        """Количество номеров на каждом этаже"""
        rooms_by_floor = Room.objects.values('floor').annotate(
            count=Count('id')
        ).order_by('floor')
        return Response(list(rooms_by_floor))


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False, methods=['get'])
    def from_city(self, request):
        """Количество клиентов из заданного города"""
        city = request.query_params.get('city', '')
        if city:
            count = Client.objects.filter(city__iexact=city).count()
            return Response({'city': city, 'count': count})
        return Response({'error': 'Не указан город'}, status=400)

    @action(detail=True, methods=['get'])
    def room_history(self, request, pk=None):
        """Клиенты, проживавшие в заданном номере в заданный период"""
        client = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({'error': 'Не указаны даты'}, status=400)

        # Находим все проживания клиента
        client_stays = Stay.objects.filter(client=client)

        # Находим клиентов, которые проживали в те же даты
        overlapping_stays = Stay.objects.filter(
            Q(check_in_date__lte=end_date) &
            Q(check_out_date__gte=start_date) &
            Q(room__in=[stay.room for stay in client_stays])
        ).exclude(client=client)

        serializer = StaySerializer(overlapping_stays, many=True)
        return Response(serializer.data)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    @action(detail=True, methods=['post'])
    def hire(self, request, pk=None):
        """Принять на работу сотрудника"""
        staff = self.get_object()
        staff.is_active = True
        staff.save()
        return Response({'status': 'сотрудник принят на работу'})

    @action(detail=True, methods=['post'])
    def fire(self, request, pk=None):
        """Уволить сотрудника"""
        staff = self.get_object()
        staff.is_active = False
        staff.save()
        return Response({'status': 'сотрудник уволен'})

    @action(detail=True, methods=['get'])
    def with_services(self, request, pk=None):
        """
        GET запрос возвращающий сотрудника с вложенными объектами услуг (многие-ко-многим)
        """
        try:
            staff = Staff.objects.prefetch_related('staffservice_set__service').get(pk=pk)
            serializer = StaffWithServicesSerializer(staff)
            return Response(serializer.data)
        except Staff.DoesNotExist:
            return Response({'error': 'Сотрудник не найден'}, status=404)



class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer

    @action(detail=False, methods=['get'])
    def cleaner_for_client_room(self, request):
        """Кто убирал номер указанного клиента в заданный день"""
        client_id = request.query_params.get('client_id')
        day_of_week = request.query_params.get('day_of_week')

        if not client_id or not day_of_week:
            return Response({'error': 'Не указаны client_id или day_of_week'}, status=400)

        try:
            client = Client.objects.get(id=client_id)
            current_stay = Stay.objects.filter(client=client, check_out_date__isnull=True).first()

            if not current_stay:
                return Response({'error': 'Клиент не проживает в настоящее время'})

            cleaner = CleaningSchedule.objects.filter(
                floor=current_stay.room.floor,
                day_of_week=day_of_week
            ).first()

            if cleaner:
                serializer = CleaningScheduleSerializer(cleaner)
                return Response(serializer.data)
            else:
                return Response({'error': 'Уборщик не найден'})

        except Client.DoesNotExist:
            return Response({'error': 'Клиент не найден'}, status=404)


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer

    @action(detail=False, methods=['get'])
    def quarterly_report(self, request):
        """Отчет о работе гостиницы за указанный квартал"""
        year = request.query_params.get('year', date.today().year)
        quarter = request.query_params.get('quarter', 1)

        try:
            year = int(year)
            quarter = int(quarter)

            # Определяем даты квартала
            quarter_starts = [date(year, 1, 1), date(year, 4, 1), date(year, 7, 1), date(year, 10, 1)]
            quarter_ends = [date(year, 3, 31), date(year, 6, 30), date(year, 9, 30), date(year, 12, 31)]

            start_date = quarter_starts[quarter - 1]
            end_date = quarter_ends[quarter - 1]

            # Статистика по номерам
            room_stats = Stay.objects.filter(
                check_in_date__lte=end_date,
                check_out_date__gte=start_date
            ).values('room__room_number', 'room__room_type__name').annotate(
                client_count=Count('client', distinct=True),
                total_income=Sum('total_cost')
            )

            # Общая статистика
            total_income = sum(item['total_income'] or 0 for item in room_stats)
            total_clients = Stay.objects.filter(
                check_in_date__lte=end_date,
                check_out_date__gte=start_date
            ).values('client').distinct().count()

            # Количество номеров по этажам
            rooms_by_floor = Room.objects.values('floor').annotate(
                room_count=Count('id')
            )

            report = {
                'period': f'{year} Q{quarter}',
                'total_income': total_income,
                'total_clients': total_clients,
                'room_statistics': list(room_stats),
                'rooms_by_floor': list(rooms_by_floor)
            }

            return Response(report)

        except (ValueError, IndexError):
            return Response({'error': 'Неверный год или квартал'}, status=400)

    @action(detail=False, methods=['post'])
    def check_in(self, request):
        """Поселить клиента"""
        client_id = request.data.get('client_id')
        room_id = request.data.get('room_id')

        try:
            client = Client.objects.get(id=client_id)
            room = Room.objects.get(id=room_id)

            if not room.is_available:
                return Response({'error': 'Номер занят'}, status=400)

            stay = Stay.objects.create(
                client=client,
                room=room,
                check_in_date=date.today()
            )

            # Помечаем номер как занятый
            room.is_available = False
            room.save()

            serializer = StaySerializer(stay)
            return Response(serializer.data)

        except (Client.DoesNotExist, Room.DoesNotExist):
            return Response({'error': 'Клиент или комната не найдены'}, status=404)

    @action(detail=True, methods=['put'])
    def update_schedule(self, request, pk=None):
        """Изменить расписание работы служащего"""
        staff = self.get_object()
        schedule_data = request.data

        # Удаляем старое расписание
        CleaningSchedule.objects.filter(staff=staff).delete()

        # Создаем новое расписание
        for schedule_item in schedule_data.get('schedule', []):
            CleaningSchedule.objects.create(
                staff=staff,
                floor=schedule_item['floor'],
                day_of_week=schedule_item['day_of_week']
            )

        return Response({'status': 'расписание обновлено'})

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        """Выселить клиента"""
        stay = self.get_object()
        stay.check_out_date = date.today()
        stay.save()

        # Освобождаем комнату
        stay.room.is_available = True
        stay.room.save()

        return Response({'status': 'клиент выселен', 'check_out_date': stay.check_out_date})

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'Система управления гостиницей - API',
        'version': '1.0',
        'documentation': 'Для доступа к API требуется аутентификация по токену',
        'public_endpoints': {
            'admin_panel': '/admin/',
            'authentication': {
                'register': 'POST /auth/users/',
                'login': 'POST /auth/token/login/',
                'logout': 'POST /auth/token/logout/',
            },
        },
        'protected_endpoints': {
            'room_types': 'GET /api/room-types/',
            'rooms': 'GET /api/rooms/',
            'clients': 'GET /api/clients/',
            'staff': 'GET /api/staff/',
            'cleaning_schedule': 'GET /api/cleaning-schedule/',
            'stays': 'GET /api/stays/',
        },
        'how_to_use': {
            '1': 'Зарегистрируйтесь: POST /auth/users/ с email, username, password',
            '2': 'Получите токен: POST /auth/token/login/ с email и password',
            '3': 'Используйте токен в заголовках: Authorization: Token ваш_токен',
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Публичный endpoint для регистрации"""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email и пароль обязательны'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Пользователь с таким email уже существует'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        email=email,
        username=username or email,
        password=password
    )

    return Response({
        'message': 'Пользователь успешно зарегистрирован',
        'user_id': user.id,
        'email': user.email,
        'next_step': 'Получите токен через POST /auth/token/login/'
    }, status=status.HTTP_201_CREATED)


from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Room

@api_view(['GET'])
@permission_classes([AllowAny])
def public_rooms_info(request):
    """Публичная информация о комнатах (без деталей)"""
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()

    return Response({
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'message': 'Для детальной информации требуется аутентификация'
    })

class HotelServiceViewSet(viewsets.ModelViewSet):
    """ViewSet для услуг гостиницы (связь многие-ко-многим)"""
    queryset = HotelService.objects.all()
    serializer_class = HotelServiceSerializer

    @action(detail=True, methods=['get'])
    def with_staff(self, request, pk=None):
        """Услуга с вложенными сотрудниками"""
        try:
            service = HotelService.objects.prefetch_related('staffservice_set__staff').get(pk=pk)
            serializer = HotelServiceSerializer(service)
            return Response(serializer.data)
        except HotelService.DoesNotExist:
            return Response({'error': 'Услуга не найдена'}, status=404)

class StaffServiceViewSet(viewsets.ModelViewSet):
    """ViewSet для связи сотрудников и услуг"""
    queryset = StaffService.objects.all()
    serializer_class = StaffServiceSerializer


from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def index(request):
    """Главная страница с фронтендом"""
    return render(request, 'hotel_app/index.html')

'''from django.views.generic import TemplateView
from django.http import HttpResponse
import os

def index(request):
    """Отдача статического HTML файла"""
    file_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    with open(file_path, 'r', encoding='utf-8') as file:
        return HttpResponse(file.read(), content_type='text/html')'''

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """Публичный endpoint для проверки статуса API"""
    return Response({
        'status': 'API работает',
        'authenticated': request.user.is_authenticated,
        'user': str(request.user) if request.user.is_authenticated else None,
        'endpoints': {
            'public': ['/api/status/', '/api/public-sample/', '/api/debug/'],
            'auth': ['/auth/token/login/', '/auth/users/'],
            'protected': ['/api/rooms/', '/api/clients/', '/api/staff/']
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def public_sample(request):
    """Публичный endpoint с примером данных"""
    from .models import Room
    from .serializers import RoomSerializer

    # Берем только 3 комнаты для примера
    rooms = Room.objects.all()[:3]
    serializer = RoomSerializer(rooms, many=True)

    return Response({
        'message': 'Это публичные данные (не требуют аутентификации)',
        'count': rooms.count(),
        'rooms': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_debug(request):
    """Endpoint для отладки API"""
    return Response({
        'status': 'API работает',
        'user': str(request.user) if request.user.is_authenticated else 'Не авторизован',
        'method': request.method,
        'path': request.path,
        'headers': dict(request.headers)
    })


@csrf_exempt
def custom_token_login(request):
    """Кастомный endpoint для входа без CSRF проверки"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            User = get_user_model()

            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    token, created = Token.objects.get_or_create(user=user)
                    return JsonResponse({
                        'auth_token': token.key,
                        'user_id': user.id,
                        'email': user.email
                    })
                else:
                    return JsonResponse({'error': 'Неверный пароль'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Пользователь не найден'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный формат данных'}, status=400)

    return JsonResponse({'error': 'Метод не разрешен'}, status=405)



from django.shortcuts import render
from rest_framework.permissions import AllowAny

# Фронтенд страницы
def login_page(request):
    return render(request, 'hotel_app/login.html')

def register_page(request):
    return render(request, 'hotel_app/register.html')

def profile_page(request):
    return render(request, 'hotel_app/profile.html')

def dashboard_page(request):
    return render(request, 'hotel_app/index.html')

