from django.db import models
from django.utils.translation import gettext_lazy as _


class ReadingRoom(models.Model):
    class RoomType(models.TextChoices):
        SMALL = "small", _("Малый зал")
        MEDIUM = "medium", _("Средний зал")
        LARGE = "large", _("Большой зал")

    number = models.PositiveIntegerField(unique=True, verbose_name="Номер зала")
    floor = models.PositiveIntegerField(verbose_name="Этаж")
    room_type = models.CharField(max_length=10, choices=RoomType.choices, verbose_name="Тип зала")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость (мест)")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена/час")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        ordering = ["number"]
        verbose_name = "Читальный зал"
        verbose_name_plural = "Читальные залы"

    def __str__(self):
        return f"Зал {self.number} (этаж {self.floor})"




class Reader(models.Model):
    library_card = models.CharField(max_length=64, unique=True, verbose_name="Номер читательского билета")
    last_name = models.CharField(max_length=64, verbose_name="Фамилия")
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    patronymic = models.CharField(max_length=64, blank=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.library_card})"




class Reservation(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name="reservations", verbose_name="Читатель")
    reading_room = models.ForeignKey(ReadingRoom, on_delete=models.PROTECT, related_name="reservations", verbose_name="Читальный зал")
    reserved_from = models.DateTimeField(verbose_name="Время начала бронирования")
    reserved_to = models.DateTimeField(null=True, blank=True, verbose_name="Время окончания бронирования")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        ordering = ["-reserved_from"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        indexes = [
            models.Index(fields=["reading_room", "reserved_from", "reserved_to"]),
            models.Index(fields=["reader", "reserved_from", "reserved_to"]),
        ]

    def __str__(self):
        return f"Бронирование {self.reader} в {self.reading_room} с {self.reserved_from}"




class Librarian(models.Model):
    last_name = models.CharField(max_length=64, verbose_name="Фамилия")
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    patronymic = models.CharField(max_length=64, blank=True, verbose_name="Отчество")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Библиотекарь"
        verbose_name_plural = "Библиотекари"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"




class Schedule(models.Model):
    class Weekday(models.IntegerChoices):
        MON = 1, _("Пн")
        TUE = 2, _("Вт")
        WED = 3, _("Ср")
        THU = 4, _("Чт")
        FRI = 5, _("Пт")
        SAT = 6, _("Сб")
        SUN = 7, _("Вс")

    librarian = models.ForeignKey(Librarian, on_delete=models.CASCADE, related_name="schedules", verbose_name="Библиотекарь")
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices, verbose_name="День недели")
    floor = models.PositiveIntegerField(verbose_name="Этаж")

    class Meta:
        unique_together = ("librarian", "weekday", "floor")
        ordering = ["librarian_id", "weekday", "floor"]
        verbose_name = "Расписание библиотекаря"
        verbose_name_plural = "Расписания библиотекарей"

    def __str__(self):
        return f"{self.librarian} — этаж {self.floor} в {self.get_weekday_display()}"

