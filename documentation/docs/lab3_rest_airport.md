# **Лабораторная работа №3**

## **Реализация серверной части на Django REST Framework**

**Дисциплина:** Web-программирование
**Исполнитель:** *Ермаков Максим Олегович*

---

# **Цель работы**

Овладеть практическими навыками разработки backend-части web-приложения с использованием Django и Django REST Framework.
Реализовать REST-API для предметной области согласно варианту, а также обеспечить авторизацию/регистрацию через Djoser.

---

# **Вариант: "Административная система аэропорта авиакомпании"**

Разрабатываемая система должна хранить и обрабатывать информацию:

* о самолетах, типах самолетов и авиакомпаниях;
* о маршрутах, рейсах, конкретных вылетах;
* о транзитных посадках;
* о пассажирах, местах и билетах;
* о сотрудниках авиакомпании (экипаже);
* о различных аналитических запросах:

  * определение наиболее часто летающей марки самолёта на маршруте;
  * поиск недозаполненных рейсов (меньше ХХ %);
  * определение свободных мест на рейс;
  * количество самолётов в ремонте;
  * количество сотрудников компании;
  * отчёт по бортам компании-владельца по маркам.

---

# **1. Подготовка проекта**

### Создание виртуального окружения:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Установка зависимостей:

```bash
pip install django djangorestframework djoser drf-yasg
```

### Создание проекта и приложения:

```bash
django-admin startproject airport_project .
python manage.py startapp airport_api
```

---

# **2. Настройка Django и DRF**

### В `settings.py` подключены приложения:

```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'airport_api',
]
```

### Добавлены настройки DRF и авторизации:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ]
}

DJOSER = {
    "LOGIN_FIELD": "username",
}
```

---

# **3. Проектирование БД и модели**

Схема базы была разработана заранее (ER-диаграмма).
Сущности отражают предметную область аэропорта.

### Пример ключевых моделей (фрагменты):

```python
class Company(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    company_type = models.CharField(max_length=20)
```

```python
class Plane(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    plane_type = models.ForeignKey(PlaneType, on_delete=models.PROTECT)
    reg_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20)
```

```python
class FlightInstance(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    plane = models.ForeignKey(Plane, on_delete=models.PROTECT)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
```

```python
class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.PROTECT)
    flight_instance = models.ForeignKey(FlightInstance, on_delete=models.CASCADE)
```

---

# **4. Миграции**

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# **5. Наполнение БД**

Создан файл `fixtures/demo_data.json`.
Данные загружены:

```bash
python manage.py loaddata airport_api/fixtures/demo_data.json
```

Теперь API возвращает реальные данные.

---

# **6. Сериализаторы (serializers.py)**

Для каждой модели создан `ModelSerializer`. Пример:

```python
class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = "__all__"
```

---

# **7. Реализация CRUD-эндпоинтов**

Для всех моделей реализованы стандартные CRUD-операции:

```python
class PlaneListCreateView(generics.ListCreateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer

class PlaneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
```

---

# **8. Вложенные GET-запросы**

## 8.1. Один-ко-многим: маршрут + рейсы

```python
class RouteWithFlightsView(generics.RetrieveAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteWithFlightsSerializer
```

Запрос:

```
GET /api/routes/<id>/with-flights/
```

## 8.2. Многие-ко-многим: вылет + экипаж

```python
class FlightInstanceWithCrewView(generics.RetrieveAPIView):
    queryset = FlightInstance.objects.all()
    serializer_class = FlightInstanceWithCrewSerializer
```

Запрос:

```
GET /api/flight-instances/<id>/with-crew/
```

---

# **9. Аналитические запросы**

Ниже — примеры реальных эндпоинтов.

## 9.1. Наиболее часто летающая марка самолёта

```python
class RouteTopPlaneTypeView(APIView):
    def get(self, request, pk):
        plane_type = (
            PlaneType.objects
            .filter(planes__flight_instances__flight__route_id=pk)
            .annotate(flights_count=Count("planes__flight_instances"))
            .order_by("-flights_count")
            .first()
        )
        ...
```

## 9.2. Недозаполненные рейсы

```python
class UnderfilledRoutesView(APIView):
    def get(self, request):
        percent = float(request.query_params.get("percent", 70))
        ...
```

## 9.3. Свободные места

```python
class FlightInstanceFreeSeatsView(APIView):
    def get(self, request, pk):
        seats = Seat.objects.filter(
            flight_instance_id=pk,
            is_booked=False,
            ticket__isnull=True,
        )
```

## 9.4. Самолёты в ремонте

```python
class PlanesInMaintenanceView(APIView):
    """
    Возвращает количество самолётов со статусом 'maintenance'.
    """
    def get(self, request):
        count = Plane.objects.filter(status="maintenance").count()
        return Response({"planes_in_maintenance": count})
```

## 9.5. Количество сотрудников компании

```python
class CompanyEmployeesCountView(APIView):
    """
    Возвращает количество активных сотрудников компании.
    """
    def get(self, request, pk):
        company_id = pk
        total = CrewMember.objects.filter(
            company_id=company_id,
            is_active=True,
        ).count()
        return Response({
            "company_id": company_id,
            "active_employees": total,
        })
```

## 9.6. Отчёт по бортам компании

```python
class CompanyPlanesReportView(APIView):
    def get(self, request, pk):
        company_id = pk

        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response({"detail": "Компания не найдена."}, status=404)

        planes_qs = Plane.objects.filter(company_id=company_id)

        total_planes = planes_qs.count()

        type_stats = (
            PlaneType.objects
            .filter(planes__in=planes_qs)
            .annotate(planes_count=Count("planes"))
            .distinct()
        )

        types_data = []
        for pt in type_stats:
            types_data.append({
                "plane_type_id": pt.id,
                "plane_type_name": pt.name,
                "seat_count": pt.seat_count,
                "cruise_speed": pt.cruise_speed,
                "planes_count": pt.planes_count,
            })

        return Response({
            "company_id": company.id,
            "company_name": company.name,
            "total_planes": total_planes,
            "by_plane_type": types_data,
        })
```

---

# **10. Авторизация и регистрация (Djoser)**

Подключены URL:

```python
path("auth/", include("djoser.urls")),
path("auth/", include("djoser.urls.authtoken")),
```

⚙️ Доступные методы:

* `POST /auth/users/` — регистрация
* `POST /auth/token/login/` — получить токен
* `POST /auth/token/logout/` — выйти
* `GET /auth/users/me/` — текущий пользователь по токену

Пример запроса:

```http
POST /auth/token/login/
{
  "username": "testuser",
  "password": "qwerty123"
}
```

---

---

# **Вывод**

В ходе лабораторной работы был создан полный REST-backend для системы учёта рейсов аэропорта:

* реализована база данных с множеством связанных сущностей;
* созданы сериализаторы, CRUD и вложенные запросы;
* реализованы сокращённые и расширенные представления данных;
* выполнены аналитические запросы согласно варианту задания;
* добавлена токен-авторизация и регистрация пользователей через Djoser;
* выполнено наполнение БД и проверка API через браузер и инструменты разработки.

Система полностью готова к использованию и дальнейшему расширению.

