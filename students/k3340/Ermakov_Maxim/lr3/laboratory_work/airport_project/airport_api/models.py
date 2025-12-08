from django.db import models


class Airport(models.Model):
    airport_code = models.CharField(
        primary_key=True,
        max_length=10,
        verbose_name="Код аэропорта (IATA/ICAO)",
    )
    country = models.CharField(max_length=100, verbose_name="Страна")
    status = models.CharField(
        max_length=20,
        verbose_name="Статус",
        help_text="Например: active / closed / maintenance",
    )
    city = models.CharField(max_length=100, verbose_name="Город")
    name = models.CharField(max_length=200, verbose_name="Название аэропорта")

    def __str__(self):
        return f"{self.airport_code} - {self.city}"


class Company(models.Model):
    COMPANY_TYPE_CHOICES = (
        ("carrier", "Авиаперевозчик"),
        ("airport_owner", "Владелец аэропорта"),
        ("ground", "Наземное обслуживание"),
        ("other", "Другое"),
    )

    name = models.CharField(max_length=200, verbose_name="Название компании")
    country = models.CharField(max_length=100, verbose_name="Страна")
    company_type = models.CharField(
        max_length=20,
        choices=COMPANY_TYPE_CHOICES,
        verbose_name="Тип компании",
    )

    def __str__(self):
        return self.name


class PlaneType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Марка / тип самолёта")
    seat_count = models.PositiveIntegerField(verbose_name="Количество мест")
    cruise_speed = models.FloatField(
        verbose_name="Крейсерская скорость (км/ч)",
    )

    def __str__(self):
        return self.name


class Plane(models.Model):
    STATUS_CHOICES = (
        ("active", "В строю"),
        ("maintenance", "В ремонте/ТО"),
        ("retired", "Списан"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="planes",
        verbose_name="Владелец борта",
    )
    plane_type = models.ForeignKey(
        PlaneType,
        on_delete=models.PROTECT,
        related_name="planes",
        verbose_name="Тип самолёта",
    )
    reg_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Бортовой номер (рег. номер)",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="Статус борта",
    )
    flight_hours = models.FloatField(
        default=0,
        verbose_name="Налёт (часы)",
    )
    last_technical_service = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата последнего ТО",
    )

    def __str__(self):
        return f"{self.reg_number} ({self.plane_type.name})"


class Route(models.Model):
    departure_airport = models.ForeignKey(
        Airport,
        on_delete=models.PROTECT,
        related_name="departing_routes",
        verbose_name="Аэропорт вылета",
    )
    destination_airport = models.ForeignKey(
        Airport,
        on_delete=models.PROTECT,
        related_name="arriving_routes",
        verbose_name="Аэропорт назначения",
    )
    distance_km = models.FloatField(verbose_name="Дистанция (км)")

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"
        constraints = [
            models.UniqueConstraint(
                fields=["departure_airport", "destination_airport"],
                name="uniq_route_departure_destination",
            )
        ]

    def __str__(self):
        return f"{self.departure_airport.airport_code} → {self.destination_airport.airport_code}"


class Flight(models.Model):
    flight_number = models.CharField(max_length=10, verbose_name="Номер рейса")
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights",
        verbose_name="Маршрут",
    )
    operating_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="operated_flights",
        verbose_name="Эксплуатант (перевозчик)",
    )

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"
        unique_together = ("flight_number", "operating_company")

    def __str__(self):
        return f"{self.flight_number} ({self.route})"



class FlightInstance(models.Model):
    STATUS_CHOICES = (
        ("scheduled", "Запланирован"),
        ("boarding", "Посадка"),
        ("departed", "Вылетел"),
        ("arrived", "Прибыл"),
        ("cancelled", "Отменён"),
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="instances",
        verbose_name="Рейс",
    )
    plane = models.ForeignKey(
        Plane,
        on_delete=models.PROTECT,
        related_name="flight_instances",
        verbose_name="Самолёт",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled",
        verbose_name="Статус вылета",
    )
    departure_time = models.DateTimeField(verbose_name="Плановое время вылета")
    departure_time_fact = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Фактическое время вылета",
    )
    arrival_time = models.DateTimeField(verbose_name="Плановое время прилёта")
    arrival_time_fact = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Фактическое время прилёта",
    )

    def __str__(self):
        return f"{self.flight.flight_number} {self.departure_time}"


class TransitStop(models.Model):
    flight_instance = models.ForeignKey(
        FlightInstance,
        on_delete=models.CASCADE,
        related_name="transit_stops",
        verbose_name="Конкретный вылет",
    )
    airport = models.ForeignKey(
        Airport,
        on_delete=models.PROTECT,
        related_name="transit_stops",
        verbose_name="Аэропорт посадки",
    )
    stop_order = models.PositiveSmallIntegerField(
        verbose_name="Порядок посадки (1,2,3...)",
    )
    arrival_time = models.DateTimeField(verbose_name="Время прилёта")
    departure_time = models.DateTimeField(verbose_name="Время вылета")

    class Meta:
        verbose_name = "Транзитная посадка"
        verbose_name_plural = "Транзитные посадки"
        ordering = ["stop_order"]

    def __str__(self):
        return f"{self.flight_instance} / {self.airport.airport_code} ({self.stop_order})"



class Passenger(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    passport_serial = models.CharField(max_length=10, verbose_name="Серия паспорта")
    passport_number = models.CharField(max_length=20, verbose_name="Номер паспорта")
    passport_region = models.CharField(
        max_length=200,
        verbose_name="Кем выдан / регион",
    )
    birth_date = models.DateField(verbose_name="Дата рождения")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="E-mail")

    def __str__(self):
        return self.full_name


class Seat(models.Model):
    SEAT_TYPE_CHOICES = (
        ("economy", "Эконом"),
        ("business", "Бизнес"),
        ("first", "Первый"),
    )

    flight_instance = models.ForeignKey(
        FlightInstance,
        on_delete=models.CASCADE,
        related_name="seats",
        verbose_name="Конкретный вылет",
    )
    seat_number = models.CharField(
        max_length=5,
        verbose_name="Номер места (например 12A)",
    )
    seat_type = models.CharField(
        max_length=20,
        choices=SEAT_TYPE_CHOICES,
        verbose_name="Класс обслуживания",
    )
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Базовая цена",
    )
    is_booked = models.BooleanField(
        default=False,
        verbose_name="Место забронировано",
    )

    class Meta:
        unique_together = ("flight_instance", "seat_number")

    def __str__(self):
        return f"{self.flight_instance} / seat {self.seat_number}"


class Ticket(models.Model):
    STATUS_CHOICES = (
        ("booked", "Бронирован"),
        ("paid", "Оплачен"),
        ("cancelled", "Отменён"),
        ("refunded", "Возврат"),
    )

    flight_instance = models.ForeignKey(
        FlightInstance,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Конкретный вылет",
    )
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Пассажир",
    )
    seat = models.OneToOneField(
        Seat,
        on_delete=models.PROTECT,
        related_name="ticket",
        verbose_name="Место",
    )
    sale_channel = models.CharField(
        max_length=50,
        verbose_name="Канал продажи",
        help_text="Например: online, касса, агент",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="booked",
        verbose_name="Статус билета",
    )
    additional_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Дополнительные сборы",
    )

    def __str__(self):
        return f"Билет {self.id} / {self.flight_instance} / {self.passenger}"



class CrewMember(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Работодатель",
    )
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения")
    education = models.CharField(max_length=200, verbose_name="Образование")
    experience_years = models.PositiveIntegerField(
        verbose_name="Стаж (лет)",
    )
    email = models.EmailField(verbose_name="E-mail")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон")
    passport_serial = models.CharField(max_length=10, verbose_name="Серия паспорта")
    passport_number = models.CharField(max_length=20, verbose_name="Номер паспорта")
    passport_region = models.CharField(
        max_length=200,
        verbose_name="Кем выдан / регион",
    )
    role = models.CharField(
        max_length=50,
        verbose_name="Роль (командир, 2й пилот, стюард и т.п.)",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Работает в компании",
    )
    is_allowed = models.BooleanField(
        default=True,
        verbose_name="Допущен к полётам",
    )

    # Many-to-many с рейсами через промежуточную таблицу Crew
    flights = models.ManyToManyField(
        "FlightInstance",
        through="Crew",
        related_name="crew_members",
        verbose_name="Рейсы",
    )

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class Crew(models.Model):
    """Промежуточная таблица: член экипажа на конкретном вылете."""

    crew_member = models.ForeignKey(
        CrewMember,
        on_delete=models.CASCADE,
        related_name="crew_assignments",
        verbose_name="Член экипажа",
    )
    flight_instance = models.ForeignKey(
        FlightInstance,
        on_delete=models.CASCADE,
        related_name="crew_assignments",
        verbose_name="Конкретный вылет",
    )
    role = models.CharField(
        max_length=50,
        verbose_name="Роль на рейсе (КВС, второй пилот, стюард)",
    )
    medical_check_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата медосмотра",
    )
    medical_status = models.CharField(
        max_length=50,
        verbose_name="Мед. статус",
        help_text="Допущен / ограниченно / недопущен",
    )
    medical_reason = models.TextField(
        blank=True,
        verbose_name="Причина ограничения/недопуска",
    )

    class Meta:
        verbose_name = "Экипаж на рейсе"
        verbose_name_plural = "Экипажи на рейсах"
        unique_together = ("crew_member", "flight_instance")

    def __str__(self):
        return f"{self.crew_member} / {self.flight_instance}"
