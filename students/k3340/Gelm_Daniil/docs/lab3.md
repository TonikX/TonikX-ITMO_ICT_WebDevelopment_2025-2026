# Лабораторная работа 3. Реализация серверной части приложения средствами Django и Django REST Framework

## Вариант 1: Система управления гостиницей

REST API для управления гостиницей на Django 3.2, Django REST Framework, Djoser и drf-yasg.

## Swagger документация

После запуска сервера доступна документация:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Модели данных

### Room (Номер)
```python
class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    floor = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    is_occupied = models.BooleanField(default=False)
```

### Guest (Клиент)
```python
class Guest(models.Model):
    passport_number = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
```

### Stay (Проживание)
```python
class Stay(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
```

### Employee (Служащий)
```python
class Employee(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
```

### CleaningSchedule (Расписание уборки)
```python
class CleaningSchedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
```

## API Endpoints

### Аутентификация

#### Регистрация
```
POST /auth/users/
{
    "username": "admin",
    "password": "password123",
    "password_retype": "password123"
}
```

#### Получение токена
```
POST /auth/token/login/
{
    "username": "admin",
    "password": "password123"
}
```

#### Текущий пользователь
```
GET /auth/users/me/
Authorization: Token <токен>
```

### Номера

- `GET /api/rooms/` - список номеров
- `POST /api/rooms/` - создать номер
- `GET /api/rooms/{id}/` - получить номер
- `PUT /api/rooms/{id}/` - обновить номер
- `DELETE /api/rooms/{id}/` - удалить номер
- `GET /api/rooms/available/` - свободные номера
- `GET /api/rooms/by_type/?type=single` - номера по типу

### Клиенты

- `GET /api/guests/` - список клиентов
- `POST /api/guests/` - создать клиента
- `GET /api/guests/{id}/` - получить клиента
- `PUT /api/guests/{id}/` - обновить клиента
- `DELETE /api/guests/{id}/` - удалить клиента
- `GET /api/guests/by_city/?city=Москва` - клиенты по городу

### Проживания

- `GET /api/stays/` - список проживаний
- `POST /api/stays/` - создать проживание
- `GET /api/stays/{id}/` - получить проживание
- `PUT /api/stays/{id}/` - обновить проживание
- `DELETE /api/stays/{id}/` - удалить проживание
- `GET /api/stays/current/` - текущие проживания
- `GET /api/stays/by_room/?room_id=1&start_date=2024-01-01&end_date=2024-01-31` - клиенты в номере за период
- `GET /api/stays/by_period/?start_date=2024-01-01&end_date=2024-01-31` - проживания за период

### Служащие

- `GET /api/employees/` - список служащих
- `POST /api/employees/` - создать служащего
- `GET /api/employees/{id}/` - получить служащего
- `PUT /api/employees/{id}/` - обновить служащего
- `DELETE /api/employees/{id}/` - удалить служащего
- `GET /api/employees/active/` - активные служащие

### Расписание уборки

- `GET /api/cleaning-schedules/` - список расписаний
- `POST /api/cleaning-schedules/` - создать расписание
- `GET /api/cleaning-schedules/{id}/` - получить расписание
- `PUT /api/cleaning-schedules/{id}/` - обновить расписание
- `DELETE /api/cleaning-schedules/{id}/` - удалить расписание
- `GET /api/cleaning-schedules/by_guest_room/?guest_id=1&day_of_week=monday` - кто убирал номер клиента

## Важные блоки кода

### Сериализаторы

```python
class StaySerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all(), source='guest', write_only=True)
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room', write_only=True)
    
    class Meta:
        model = Stay
        fields = ['id', 'guest', 'guest_id', 'room', 'room_id', 'check_in_date', 'check_out_date']
```

### ViewSets

```python
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['room_type', 'floor', 'is_occupied']
    search_fields = ['number', 'phone']
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        rooms = self.queryset.filter(is_occupied=False)
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)
```

### Настройки REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## Установка и запуск

1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. Выполнить миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

4. Запустить сервер:
```bash
python manage.py runserver
```

## Использование API

Все запросы требуют токена в заголовке:
```
Authorization: Token <токен>
```

Пример:
```bash
curl -X GET http://localhost:8000/api/rooms/ \
  -H "Authorization: Token <токен>"
```

