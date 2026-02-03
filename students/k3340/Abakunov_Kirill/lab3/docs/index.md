# Отчет по лабораторной работе №3

**Выполнил:** Абакунов Кирилл, группа K3340  
**Цель:** овладеть практическими навыками разработки web‑сервисов средствами Django 3, Django REST Framework, Djoser и PostgreSQL.  
**Вариант:** программная система для администратора гостиницы.

## 1) Используемые технологии

- **Python 3.9**
- **Django 3.2** + **Django REST Framework**
- **Djoser** (регистрация/логин по токенам)
- **PostgreSQL** (через Docker Compose)
- **Swagger UI / ReDoc** (drf-yasg)

## 2) Модель данных (Django ORM)

### Room (номер)

- **Поля:** `number` (unique), `room_type` (single/double/triple), `floor` (>=1), `phone`, `price_per_day` (>=0)
- **Смысл:** хранит постоянные характеристики номера (тип, этаж, телефон, цена).

### Guest (клиент)

- **Поля:** `passport_number` (unique), `last_name`, `first_name`, `middle_name`, `city`, `check_in_date`, `check_out_date` (nullable), `room` (FK → Room, `PROTECT`)
- **Ограничение:** `check_out_date >= check_in_date` (валидация).
- **Смысл:** хранит историю проживания (заселение/выселение) и «текущность» через `check_out_date`.

### Staff (служащий)

- **Поля:** ФИО, `is_active`, `hire_date`, `fire_date` (nullable)
- **Ограничение:** `fire_date >= hire_date` (валидация).
- **Смысл:** сотрудники гостиницы; увольнение отмечается `is_active=False`.

### CleaningSchedule (расписание уборки)

- **Поля:** `staff` (FK → Staff, `CASCADE`), `floor` (>=1), `weekday` (1..7)
- **Ограничение уникальности:** `(staff, floor, weekday)` уникально.
- **Смысл:** один сотрудник может убирать разные этажи в разные дни.

### Важные фрагменты кода (модели)

Суть проверки доступности номера реализована методом `Room.is_available(...)`:

```9:57:/Users/abakunov/Desktop/web-itmo/lab3/api/models.py
class Room(models.Model):
    # ...
    def is_available(self, check_in_date=None, check_out_date=None):
        """Проверка доступности номера"""
        from django.utils import timezone

        if check_in_date is None:
            check_in_date = timezone.now().date()

        # Ищем активные бронирования
        active_guests = self.guests.filter(
            check_in_date__lte=check_in_date,
        ).filter(
            models.Q(check_out_date__isnull=True) |
            models.Q(check_out_date__gte=check_in_date)
        )

        if check_out_date:
            active_guests = active_guests.filter(
                check_in_date__lt=check_out_date
            )

        return not active_guests.exists()
```

Ограничение уникальности расписания:

```161:171:/Users/abakunov/Desktop/web-itmo/lab3/api/models.py
class CleaningSchedule(models.Model):
    # ...
    class Meta:
        verbose_name = 'Расписание уборки'
        verbose_name_plural = 'Расписания уборки'
        ordering = ['weekday', 'floor']
        unique_together = ['staff', 'floor', 'weekday']
```

## 3) API (DRF): основные эндпоинты

Маршрутизация реализована через DRF Router:

```11:20:/Users/abakunov/Desktop/web-itmo/lab3/api/urls.py
router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'guests', GuestViewSet, basename='guest')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'schedules', CleaningScheduleViewSet, basename='schedule')
router.register(r'reports', ReportViewSet, basename='report')
```

### 3.1 Номера (`/api/rooms/`)

- **CRUD:** `GET/POST /api/rooms/`, `GET/PATCH/PUT/DELETE /api/rooms/{id}/`
- **Свободные номера (по заданию):** `GET /api/rooms/available/`
- **Клиенты в номере за период (по заданию):** `GET /api/rooms/{id}/guests_history/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

Ключевые actions:

```19:80:/Users/abakunov/Desktop/web-itmo/lab3/api/views.py
class RoomViewSet(viewsets.ModelViewSet):
    # ...
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Получить список свободных номеров"""
        # ...

    @action(detail=True, methods=['get'])
    def guests_history(self, request, pk=None):
        """История клиентов в номере"""
        # ...
```

### 3.2 Клиенты (`/api/guests/`)

- **CRUD:** `GET/POST /api/guests/`, `GET/PATCH/PUT/DELETE /api/guests/{id}/`
- **Текущие гости:** `GET /api/guests/current/`
- **Клиенты из города (по заданию):** `GET /api/guests/from_city/?city=...`
- **Кто убирал номер клиента (по заданию):** `GET /api/guests/{id}/cleaning_staff/?weekday=1..7`
- **Клиенты, проживавшие одновременно (по заданию):** `GET /api/guests/{id}/concurrent_guests/?start_date=...&end_date=...`
- **Поселить (по заданию):** `POST /api/guests/check_in/`
- **Выселить (по заданию):** `PATCH /api/guests/{id}/check_out/`

### 3.3 Служащие (`/api/staff/`)

- **CRUD:** `GET/POST /api/staff/`, `GET/PATCH/PUT/DELETE /api/staff/{id}/`
- **Работающие:** `GET /api/staff/active/`
- **Принять (по заданию):** `POST /api/staff/hire/`
- **Уволить (по заданию):** `PATCH /api/staff/{id}/fire/`

### 3.4 Расписание уборки (`/api/schedules/`)

- **CRUD (изменение расписания по заданию):** `GET/POST /api/schedules/`, `GET/PATCH/PUT/DELETE /api/schedules/{id}/`
- **По этажу:** `GET /api/schedules/by_floor/?floor=...`
- **По дню недели:** `GET /api/schedules/by_weekday/?weekday=1..7`

## 4) Отчет за квартал (по заданию)

Эндпоинт:
- `GET /api/reports/quarterly/?year=YYYY&quarter=1..4`

Выходные данные включают:
- число клиентов за период **по каждому номеру**
- количество номеров **по этажам**
- доход **по каждому номеру**
- суммарный доход **по гостинице**

Ключевой блок расчета дохода:

```428:475:/Users/abakunov/Desktop/web-itmo/lab3/api/views.py
for room in rooms:
    guests = Guest.objects.filter(
        room=room,
        check_in_date__lte=end_date
    ).filter(
        Q(check_out_date__isnull=True) | Q(check_out_date__gte=start_date)
    )

    room_income = 0
    for guest in guests:
        stay_start = max(guest.check_in_date, start_date)
        stay_end = min(
            guest.check_out_date if guest.check_out_date else end_date,
            end_date
        )
        days = (stay_end - stay_start).days + 1
        room_income += days * float(room.price_per_day)
```

## 5) Аутентификация и документация API

Подключение Djoser и Swagger:

```22:32:/Users/abakunov/Desktop/web-itmo/lab3/hotel_system/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
```

Основные auth эндпоинты:
- `POST /api/auth/users/` — регистрация
- `POST /api/auth/token/login/` — получить токен
- `GET /api/auth/users/me/` — текущий пользователь

## 6) Тестовые данные (автозаполнение)

Для заполнения БД реализована команда `load_hotel_data` (номера/служащие/расписание/гости):

```14:50:/Users/abakunov/Desktop/web-itmo/lab3/api/management/commands/load_hotel_data.py
class Command(BaseCommand):
    help = 'Загрузка тестовых данных в базу данных гостиницы'

    def handle(self, *args, **options):
        # ...
        rooms = self.create_rooms()
        staff = self.create_staff()
        schedules = self.create_cleaning_schedules(staff, rooms)
        guests = self.create_guests(rooms)
        # ...
```

## 7) Запуск проекта

```bash
cd lab3
docker-compose up --build
```

После запуска:
- Swagger UI: `http://localhost:8000/swagger/`
- Admin: `http://localhost:8000/admin/` (логин/пароль: `admin` / `admin123`)
