# Django REST Framework API для управления дронами

В рамках лабораторной работы реализовано REST API приложение **dronepass** для управления дронами, полётами, логами полётов и документами. Проект использует Django REST Framework, Djoser для аутентификации и PostgreSQL в качестве базы данных.

## Архитектура проекта

Проект состоит из двух основных приложений:

- **accounts** - управление пользователями и профилями
- **drones** - управление дронами, полётами, логами и документами

## Фичи

- Аутентификация через Djoser с JWT токенами
- Автоматическое создание профиля при регистрации пользователя
- CRUD операции для дронов, полётов, логов полётов и документов
- Вложенные эндпоинты для удобной работы со связанными данными
- Оптимизация запросов через `select_related` и `prefetch_related`
- Загрузка файлов (аватары пользователей)
- Разделение прав доступа (только авторизованные пользователи)

## Модели данных

### Приложение accounts

Модель `Profile` расширяет стандартную модель User (Djoser) дополнительной информацией:

```python
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, ...)
    display_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Приложение drones

Реализованы четыре основные модели:

**Drones** - информация о дронах:

- Производитель, модель, серийный номер
- Категория (любительский, коммерческий, профессиональный)
- Статус (активен, требуется проверка, архивирован)
- Технические характеристики (вес, размеры, скорость, дальность полёта)
- Наличие камеры

**Flights** - информация о полётах:

- Связь с дроном (ForeignKey)
- Дата и время начала/окончания полёта
- Регион полёта, причина полёта
- Дистанция, использование батареи
- Заметки

**FlightLogs** - логи полётов:

- Связь с полётом (ForeignKey)
- Временная метка, координаты (широта, долгота)
- Высота полёта, заряд батареи
- Сообщение

**Documents** - документы дронов:

- Связь с дроном (ForeignKey)
- Тип документа (сертификат, страховка, фото, лицензия, прочее)
- URL файла
- Дата загрузки

## Реализация

### Аутентификация и профили

#### Настройка Djoser

В `settings.py` настроен Djoser для работы с username как логином:

```python
DJOSER = {
    "USER_ID_FIELD": "id",
    "LOGIN_FIELD": "username",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SERIALIZERS": {
        "user_create": "accounts.serializers.UserCreateSerializer",
        "user": "djoser.serializers.UserSerializer",
        "current_user": "djoser.serializers.UserSerializer",
    },
    "PERMISSIONS": {
        "user": ["rest_framework.permissions.IsAuthenticated"],
        "user_list": ["rest_framework.permissions.IsAuthenticated"],
    },
}
```

#### Автоматическое создание профиля

Реализован сигнал для автоматического создания профиля при регистрации пользователя:

```python
@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """
    Создание профиля для нового пользователя
    """
    if created:
        Profile.objects.get_or_create(user=instance)
```

Сигнал подключён в `apps.py`:

```python
class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals
```

#### Эндпоинты для профилей

Реализованы два эндпоинта для работы с профилями:

**GET/PATCH /api/profile/** - получение и обновление своего профиля:

```python
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.select_related("user").get_or_create(
            user=self.request.user
        )
        return profile
```

**GET /api/users/<id>/profile/** - просмотр профиля другого пользователя:

```python
class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "user_id"

    def get_object(self):
        user_id = self.kwargs[self.lookup_url_kwarg]
        return get_object_or_404(
            Profile.objects.select_related("user"), user__id=user_id
        )
```

### CRUD операции для дронов

#### Базовый класс для аутентификации

Создан базовый класс `AuthenticatedModelViewSet`, который требует аутентификацию на всех эндпоинтах:

```python
class AuthenticatedModelViewSet(viewsets.ModelViewSet):
    """
    Базовый класс, который требует аутентификацию на каждом эндпоинте
    """
    permission_classes = [permissions.IsAuthenticated]
```

#### ViewSet для дронов

```python
class DroneViewSet(AuthenticatedModelViewSet):
    serializer_class = DroneSerializer

    def get_queryset(self):
        return (
            Drones.objects.all()
            .prefetch_related("flights", "documents")
            .order_by("id")
        )
```

Используется `prefetch_related` для оптимизации запросов к связанным данным (полёты и документы).

#### ViewSet для полётов

```python
class FlightViewSet(AuthenticatedModelViewSet):
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = Flights.objects.select_related("drone_id").prefetch_related("logs").order_by("-start_datetime")
        drone_pk = self.kwargs.get("drone_pk")
        if drone_pk:
            queryset = queryset.filter(drone_id_id=drone_pk)
        return queryset

    def perform_create(self, serializer):
        drone_pk = self.kwargs.get("drone_pk")
        if drone_pk:
            drone = get_object_or_404(Drones, pk=drone_pk)
            serializer.save(drone_id=drone)
        else:
            serializer.save()
```

Поддерживает как обычный доступ, так и вложенный доступ через `/drones/<id>/flights/`.

#### ViewSet для логов полётов

```python
class FlightLogViewSet(AuthenticatedModelViewSet):
    serializer_class = FlightLogSerializer

    def get_queryset(self):
        queryset = FlightLogs.objects.select_related("flight_id", "flight_id__drone_id").order_by("-timestamp")
        flight_pk = self.kwargs.get("flight_pk")
        if flight_pk:
            queryset = queryset.filter(flight_id_id=flight_pk)
        return queryset

    def perform_create(self, serializer):
        flight_pk = self.kwargs.get("flight_pk")
        if flight_pk:
            flight = get_object_or_404(Flights, pk=flight_pk)
            serializer.save(flight_id=flight)
        else:
            serializer.save()
```

Поддерживает вложенный доступ через `/flights/<id>/logs/`.

#### ViewSet для документов

```python
class DocumentViewSet(AuthenticatedModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Documents.objects.select_related("drone_id").order_by("-uploaded_at")
        drone_pk = self.kwargs.get("drone_pk")
        if drone_pk:
            queryset = queryset.filter(drone_id_id=drone_pk)
        return queryset

    def perform_create(self, serializer):
        drone_pk = self.kwargs.get("drone_pk")
        if drone_pk:
            drone = get_object_or_404(Drones, pk=drone_pk)
            serializer.save(drone_id=drone)
        else:
            serializer.save()
```

Поддерживает вложенный доступ через `/drones/<id>/documents/`.

### Вложенные роутеры

Для удобной работы со связанными данными используется библиотека `drf-nested-routers`:

```python
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r"drones", DroneViewSet, basename="drone")
router.register(r"flights", FlightViewSet, basename="flight")
router.register(r"logs", FlightLogViewSet, basename="log")
router.register(r"documents", DocumentViewSet, basename="document")

# Вложенные роутеры для дронов
drones_router = routers.NestedDefaultRouter(router, r"drones", lookup="drone")
drones_router.register(r"flights", FlightViewSet, basename="drone-flights")
drones_router.register(r"documents", DocumentViewSet, basename="drone-documents")

# Вложенный роутер для полётов
flights_router = routers.NestedDefaultRouter(router, r"flights", lookup="flight")
flights_router.register(r"logs", FlightLogViewSet, basename="flight-logs")
```

Это позволяет обращаться к связанным данным через удобные URL:
- `/api/drones/<id>/flights/` - все полёты конкретного дрона
- `/api/drones/<id>/documents/` - все документы конкретного дрона
- `/api/flights/<id>/logs/` - все логи конкретного полёта

## Эндпоинты API

### Аутентификация (Djoser)

- `POST /auth/users/` - регистрация нового пользователя
- `POST /auth/jwt/create/` - получение JWT токена
- `POST /auth/jwt/refresh/` - обновление JWT токена
- `GET /auth/users/me/` - информация о текущем пользователе

### Профили

- `GET /api/profile/` - получение своего профиля
- `PATCH /api/profile/` - обновление своего профиля
- `GET /api/users/<id>/profile/` - просмотр профиля другого пользователя

### Дроны

- `GET /api/drones/` - список всех дронов
- `POST /api/drones/` - создание нового дрона
- `GET /api/drones/<id>/` - детальная информация о дроне
- `PUT /api/drones/<id>/` - полное обновление дрона
- `PATCH /api/drones/<id>/` - частичное обновление дрона
- `DELETE /api/drones/<id>/` - удаление дрона

### Полёты

- `GET /api/flights/` - список всех полётов
- `POST /api/flights/` - создание нового полёта
- `GET /api/flights/<id>/` - детальная информация о полёте
- `PUT /api/flights/<id>/` - полное обновление полёта
- `PATCH /api/flights/<id>/` - частичное обновление полёта
- `DELETE /api/flights/<id>/` - удаление полёта

**Вложенные эндпоинты:**
- `GET /api/drones/<id>/flights/` - все полёты конкретного дрона
- `POST /api/drones/<id>/flights/` - создание полёта для конкретного дрона

### Логи полётов

- `GET /api/logs/` - список всех логов
- `POST /api/logs/` - создание нового лога
- `GET /api/logs/<id>/` - детальная информация о логе
- `PUT /api/logs/<id>/` - полное обновление лога
- `PATCH /api/logs/<id>/` - частичное обновление лога
- `DELETE /api/logs/<id>/` - удаление лога

**Вложенные эндпоинты:**
- `GET /api/flights/<id>/logs/` - все логи конкретного полёта
- `POST /api/flights/<id>/logs/` - создание лога для конкретного полёта

### Документы

- `GET /api/documents/` - список всех документов
- `POST /api/documents/` - создание нового документа
- `GET /api/documents/<id>/` - детальная информация о документе
- `PUT /api/documents/<id>/` - полное обновление документа
- `PATCH /api/documents/<id>/` - частичное обновление документа
- `DELETE /api/documents/<id>/` - удаление документа

**Вложенные эндпоинты:**
- `GET /api/drones/<id>/documents/` - все документы конкретного дрона
- `POST /api/drones/<id>/documents/` - создание документа для конкретного дрона

## Оптимизация запросов

Для повышения производительности используются оптимизации запросов к базе данных:

- `select_related()` - для ForeignKey связей (один запрос вместо N+1)
- `prefetch_related()` - для ManyToMany и обратных ForeignKey связей

## Безопасность

- Все эндпоинты требуют аутентификации (кроме регистрации и получения токена)
- Используется JWT аутентификация через Djoser
- Пользователи могут просматривать профили других пользователей, но редактировать только свой
- Все CRUD операции доступны только авторизованным пользователям

## Технологии

- **Django 5.2.6** - веб-фреймворк
- **Django REST Framework** - для создания REST API
- **Djoser** - для аутентификации и управления пользователями
- **PostgreSQL** - база данных
- **drf-nested-routers** - для вложенных роутеров
- **JWT** - для токенов аутентификации
