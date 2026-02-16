# Отчет по Лабораторной работе №3

## Тема: Реализация серверной части приложения средствами Django и Django REST Framework

> **Выполнил:** Христофоров Владислав Николаевич, K3340, WEB 2.3
>
> **Вариант:** Администратор гостиницы

### 1. Цель работы

Овладеть практическими навыками реализации web-сервисов средствами Django и Django REST Framework (DRF). Создать серверную часть приложения для предметной области "Гостиница", настроить взаимодействие с реляционной базой данных (PostgreSQL), реализовать API для CRUD-операций с фильтрацией и настроить систему авторизации.

### 2. Задание

Разработать информационную систему для администратора гостиницы.

**Основные требования:**

1. **Учет номеров:** В гостинице есть номера трех типов (одноместный, двухместный, трехместный), которые отличаются стоимостью и вместимостью.

2. **Учет клиентов:** Хранение данных о постояльцах (ФИО, паспорт, город).

3. **Учет сотрудников:** Хранение данных о персонале и графике уборки этажей.

4. **Бизнес-логика:**
    - Заселение клиентов в номера (учет дат заезда/выезда).

    - Контроль вместимости (нельзя заселить в номер больше людей, чем положено, с учетом пересечения дат).

    - Расчет стоимости проживания (автоматически при сохранении брони).

    - Получение списков с фильтрацией (по городу, статусу номера и т.д.).

5. **Технологии:** Django ORM, DRF, Djoser, PostgreSQL.

### 3. Описание предметной области и структуры БД

Для реализации системы была спроектирована база данных, соответствующая **3-й нормальной форме**.

#### 3.1. Типы сущностей (Классификация по Э. Кодду)

- **Стержневые:** `Floor` (Этаж), `Room` (Номер), `Guest` (Клиент), `Employee` (Сотрудник). Независимые сущности.

- **Характеристические:** `RoomType` (Тип номера), `City` (Город). Справочники, уточняющие свойства стержневых сущностей.

- **Ассоциативные:**
    - `Booking` (Бронирование): Связывает `Guest` и `Room` во времени.

    - `CleaningSchedule` (График уборки): Связывает `Employee`, Этаж и День недели.

#### 3.2. Описание моделей (Таблицы)

| Модель               | Тип                | Описание      | Ключевые поля                                               |
| -------------------- | ------------------ | ------------- | ----------------------------------------------------------- |
| **RoomType**         | Характеристическая | Типы номеров  | `name`, `max_guests`, `price`                               |
| **City**             | Характеристическая | Города        | `name`                                                      |
| **Floor**            | Стержневая         | Этажи         | `number`                                                    |
| **Room**             | Стержневая         | Номера        | `number`, `room_type` (FK), `floor` (FK), `phone`, `status` |
| **Guest**            | Стержневая         | Клиенты       | `passport`, `fio`, `city` (FK)                              |
| **Booking**          | Ассоциативная      | Бронирование  | `guest` (FK), `room` (FK), `check_in`, `check_out`          |
| **Employee**         | Стержневая         | Сотрудники    | `fio`                                                       |
| **CleaningSchedule** | Ассоциативная      | График уборки | `employee` (FK), `floor` (FK), `day_of_week`                |

#### 3.3. ER-диаграмма (Схема связей)

```mermaid
erDiagram
    City ||--o{ Guest : "from"
    Guest ||--o{ Booking : "makes"
    Room ||--o{ Booking : "booked in"


    RoomType ||--o{ Room : "has type"
    Floor ||--o{ Room : "located on"
    Floor ||--o{ CleaningSchedule : "cleaned on"
    Employee ||--o{ CleaningSchedule : "assigned to"



```

### 4. Ход выполнения работы

#### 4.1. Инициализация проекта

1. Создана директория проекта и виртуальное окружение.
2. Установлены необходимые библиотеки: `Django`, `djangorestframework`, `psycopg2-binary`, `python-dotenv`, `djoser`.
3. Инициализирован Django-проект `hotel_project` и создано приложение `hotel_app`

```bash
django-admin startproject hotel_project
cd hotel_project
python manage.py startapp hotel_app
```

**Настройка БД (PostgreSQL):** В файле `settings.py` настроено подключение к PostgreSQL через переменные окружения (`.env`):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

```

#### 4.2. Реализация моделей (models.py)

В файле `models.py` описаны классы моделей. Для обеспечения целостности данных использован метод `clean()`, реализующий бизнес-логику (проверка дат, статуса ремонта и переполнения номера).

**Фрагмент кода (Модель Booking с валидацией):**

```python
class Booking(models.Model):
    """Бронирование"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Номер", related_name="bookings")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="Гость", related_name="bookings")
    check_in = models.DateField(verbose_name="Дата заезда")
    check_out = models.DateField(verbose_name="Дата выезда", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Итого")


    def clean(self):
        """Проверка бизнес-логики"""
        # 1. Проверка дат
        if self.check_out and self.check_out < self.check_in:
            raise ValidationError("Дата выезда не может быть раньше даты заезда!")

        # 2. Проверка статуса номера (ремонт)
        if self.is_active and self.room.status == 'maintenance':
            raise ValidationError(f"Номер {self.room.number} находится на обслуживании!")

        # 3. Проверка на переполнение (с учетом дат)
        if self.is_active:
            check_out_date = self.check_out if self.check_out else (datetime.date.today() + datetime.timedelta(days=3650))

            overlapping_bookings = Booking.objects.filter(
                room=self.room,
                is_active=True,
                check_in__lt=check_out_date
            ).exclude(pk=self.pk)

            actual_overlaps = []
            for b in overlapping_bookings:
                b_end = b.check_out if b.check_out else (datetime.date.today() + datetime.timedelta(days=3650))
                if b_end > self.check_in:
                    actual_overlaps.append(b)

            capacity = self.room.room_type.max_guests
            if len(actual_overlaps) >= capacity:
                 raise ValidationError(f"Номер {self.room.number} занят на выбранные даты!")

    def save(self, *args, **kwargs):
        self.clean()
        if self.check_out:
            days = (self.check_out - self.check_in).days
            if days == 0: days = 1
            self.total_cost = days * self.room.room_type.price

            # Автоматическое освобождение, если дата выезда прошла или сегодня
            if self.check_out <= timezone.now().date():
                self.room.status = 'free'
                self.room.save()
        else:
            self.room.status = 'occupied'
            self.room.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest} -> {self.room}"
```

**Миграции:**
После описания моделей были созданы и применены миграции.

```
python manage.py makemigrations
python manage.py migrate
```

#### 4.3. Наполнение базы данных

Модели были зарегистрированы в файле `hotel_app/admin.py`. База данных была наполнена тестовыми данными (города, типы номеров, этажи, сотрудники, гости) для проверки работоспособности системы.

- Города: Москва, Санкт-Петербург, Сочи и др.
- Типы номеров: Эконом, Стандарт, Комфорт, Люкс, Президентский
- Этажи: 1-5.
- Номера: 101, 102, 205 и т.д.
- Сотрудники и их графики уборки.
- Гости и записи о бронировании.

**Пример данных:**

<table style="border: none; border-collapse: collapse; width: 100%;">
    <tr style="border: none;">
        <td style="border: none; vertical-align: top; width: 25%; padding: 5px;">
            <img src="../img-lab-3/admin_models.png" style="width: 100%;">
        </td>
        <td style="border: none; vertical-align: top; width: 25%; padding: 5px;">
            <img src="../img-lab-3/rooms.png" style="width: 100%;">
        </td>
        <td style="border: none; vertical-align: top; width: 20%; padding: 5px;">
            <img src="../img-lab-3/guests.png" style="width: 100%;">
        </td>
        <td style="border: none; vertical-align: top; width: 30%; padding: 5px;">
            <img src="../img-lab-3/bookings.png" style="width: 100%;">
        </td>
    </tr>
</table>

### 5. Реализация API (DRF)

#### 5.1. Сериализаторы (serializers.py)

Для преобразования моделей в JSON использованы `ModelSerializer`.

- Для **чтения (`GET`)** реализована вложенная сериализация (Nested Serializers), чтобы вместо ID связанных объектов (например, типа номера) выводилась полная информация о них.
- Для **записи (`POST/PUT`)** используются стандартные поля `PrimaryKeyRelatedField`, принимающие ID.
- В `BookingSerializer` реализован метод `validate`, который вызывает логику `clean()` модели.

**Фрагмент кода (Сериализатор Booking с валидацией):**

```python
class BookingSerializer(serializers.ModelSerializer):
    guest_details = GuestSerializer(source='guest', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)

    guest = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    is_active = serializers.BooleanField(default=True, initial=True)

    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, data):
        instance_data = {}
        if self.instance:
            instance_data = {
                'room': self.instance.room, 'guest': self.instance.guest,
                'check_in': self.instance.check_in, 'check_out': self.instance.check_out,
                'is_active': self.instance.is_active
            }
        instance_data.update(data)

        try:
            temp_instance = Booking(**instance_data)
        except TypeError:
            return data

        if self.instance:
            temp_instance.pk = self.instance.pk

        try:
            temp_instance.clean()
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                raise serializers.ValidationError(e.message_dict)
            else:
                raise serializers.ValidationError(e.messages)
        return data
```

#### 5.2. Представления (Views) и Фильтрация

Использованы `Generics` (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`) для реализации полного набора CRUD-операций для всех моделей. Подключена фильтрация `django-filters`.

**Фрагмент кода (Представления для бронирований):**

```python
class BookingList(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['guest__last_name', 'room__number', 'is_active', 'check_in']

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
```

#### 5.3 Описание реализованных эндпоинтов

В соответствии с заданием, реализован API, покрывающий все сущности.

| Метод         | URL                   | Описание                                               |
| ------------- | --------------------- | ------------------------------------------------------ |
| GET, POST     | `/api/rooms/`         | Список номеров / Создать номер (фильтры: статус, этаж) |
| GET, PUT, DEL | `/api/rooms/{id}/`    | Детали номера, изменение, удаление                     |
| GET, POST     | `/api/guests/`        | Список гостей (фильтр: город, фамилия)                 |
| GET, PUT, DEL | `/api/guests/{id}/`   | Детали гостя                                           |
| GET, POST     | `/api/bookings/`      | Список бронирований (фильтр: гость, номер, даты)       |
| GET, PUT, DEL | `/api/bookings/{id}/` | Управление конкретной бронью                           |
| GET, POST     | `/api/employees/`     | Список сотрудников                                     |
| GET, POST     | `/api/schedules/`     | Графики уборки                                         |
| GET           | `/api/room-types/`    | Справочник типов номеров                               |
| GET           | `/api/cities/`        | Справочник городов                                     |

### 6. Примеры работы системы

#### Сценарий 1: Просмотр и фильтрация бронирований

Администратор запрашивает список бронирований комнаты 101.

`GET /api/bookings/?room__number=101`

![api_bookings](img-lab-3/api_bookings_room.png){ width=60% }

#### Сценарий 2: Заселение гостя (Валидация бизнес-логики)

Администратор пытается заселить гостя.

`POST /api/bookings/`

- **Кейс А (Успех):** Заселение в свободный номер.

    <table style="border: none; border-collapse: collapse; width: 100%;">
        <tr style="border: none;">
            <td style="border: none; vertical-align: top; width: 50%; padding: 5px;">
                <img src="../img-lab-3/post_booking_form_success.png" style="width: 100%;">
            </td>
            <td style="border: none; vertical-align: top; width: 50%; padding: 5px;">
                <img src="../img-lab-3/post_booking_success.png" style="width: 100%;">
            </td>
        </tr>
    </table>

- **Кейс Б (Ошибка):** Попытка заселить гостя в номер, который находится на ремонте. Система возвращает ошибку `400 Bad Request`.

    <table style="border: none; border-collapse: collapse; width: 100%;">
        <tr style="border: none;">
            <td style="border: none; vertical-align: top; width: 50%; padding: 5px;">
                <img src="../img-lab-3/post_booking_form_failure.png" style="width: 100%;">
            </td>
            <td style="border: none; vertical-align: top; width: 50%; padding: 5px;">
                <img src="../img-lab-3/post_booking_failure.png" style="width: 100%;">
            </td>
        </tr>
    </table>

### 7. Авторизация и Аутентификация (Djoser)

Подключена библиотека `Djoser` для управления пользователями. Реализована аутентификация по токенам.

**Конфигурация (urls.py):**

```python
path('auth/', include('djoser.urls')),
path('auth/', include('djoser.urls.authtoken')),

```

1. **Регистрация пользователя:** `POST /auth/users/`
2. **Вход в систему:** `POST /auth/token/login/`

**Регистрация пользователя:**

![auth_users](img-lab-3/auth_users.png){ width=60% }

**Успешное получение токена при входе:**

![token_create](img-lab-3/token_create.png){ width=60% }

### Заключение

В результате выполнения лабораторной работы успешно спроектирована и реализована серверная часть системы для администратора гостиницы, включающая нормализованную базу данных (3НФ) (PostgreSQL) с учетом бизнес-логики предметной области, полноценный REST API на DRF с поддержкой CRUD, вложенной сериализации и фильтрацией, а также система авторизации на базе токенов.
