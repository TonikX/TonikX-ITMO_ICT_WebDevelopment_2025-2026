from django.db import models


class Room(models.Model):
    """
    Модель гостиничного номера
    """

    class RoomType(models.TextChoices):
        # Возможные типы номеров
        SINGLE = "S", "Одноместный"
        DOUBLE = "D", "Двухместный"
        TRIPLE = "T", "Трехместный"

    # Номер комнаты (уникальный)
    number = models.PositiveIntegerField(unique=True)

    # Этаж
    floor = models.PositiveIntegerField()

    # Тип номера (одноместный / двухместный / трехместный)
    type = models.CharField(
        max_length=1,
        choices=RoomType.choices
    )

    # Цена за сутки проживания
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Телефон в номере
    phone = models.CharField(max_length=32)

    def __str__(self):
        # Как объект будет выглядеть в админке и shell
        return f"Room {self.number}"


class Client(models.Model):
    """
    Клиент гостиницы
    """

    # Паспортные данные (уникальны)
    passport_number = models.CharField(max_length=32, unique=True)

    # ФИО
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64, blank=True)

    # Город, откуда приехал клиент
    city_from = models.CharField(max_length=128)

    # Адрес клиента
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Stay(models.Model):
    """
    Проживание клиента в номере за определённый период
    """

    # Клиент, который проживает
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,   # при удалении клиента удаляем проживания
        related_name="stays"        # client.stays.all()
    )

    # Номер, в котором проживает клиент
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,   # при удалении номера удаляем проживания
        related_name="stays"        # room.stays.all()
    )

    # Дата заезда
    check_in = models.DateField()

    # Дата выезда (NULL = ещё проживает)
    check_out = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        # Удобный вывод проживания
        return f"{self.client} -> {self.room}"


class Employee(models.Model):
    """
    Сотрудник гостиницы (уборщик)
    """

    # ФИО сотрудника
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64, blank=True)

    # Активен ли сотрудник (учитывается в аналитике)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CleaningSchedule(models.Model):
    """
    График уборки: кто, какой этаж и в какой день недели убирает
    """

    class Weekday(models.IntegerChoices):
        # Дни недели (0 = понедельник)
        MON = 0, "Понедельник"
        TUE = 1, "Вторник"
        WED = 2, "Среда"
        THU = 3, "Четверг"
        FRI = 4, "Пятница"
        SAT = 5, "Суббота"
        SUN = 6, "Воскресенье"

    # Сотрудник, выполняющий уборку
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="schedules"
    )

    # Этаж, который он убирает
    floor = models.PositiveIntegerField()

    # День недели
    weekday = models.IntegerField(
        choices=Weekday.choices
    )

    class Meta:
        # Один сотрудник не может убирать один этаж в один день дважды
        unique_together = ("employee", "floor", "weekday")