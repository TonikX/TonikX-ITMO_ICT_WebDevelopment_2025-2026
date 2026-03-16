from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название клуба")
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=150, verbose_name="Контактное лицо")
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Alpinist(models.Model):
    name = models.CharField(max_length=150, verbose_name="ФИО")
    address = models.TextField(verbose_name="Адрес")
    clubs = models.ManyToManyField(
        Club,
        blank=True,
        related_name="members",
        verbose_name="Клубы",
    )

    def __str__(self):
        return self.name

class Mountain(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название горы")
    height = models.PositiveIntegerField(verbose_name="Высота (метры)")
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, verbose_name="Район")

    def __str__(self):
        return f"{self.name} ({self.height}м)"

    class Meta:
        ordering = ['id']

class Route(models.Model):
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE, related_name="routes")
    description = models.TextField(verbose_name="Описание маршрута")
    expected_duration = models.DurationField(verbose_name="Продолжительность (план)")

    def __str__(self):
        return f"Маршрут на {self.mountain.name}"

class Climb(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="climbs")
    start_planned = models.DateTimeField(verbose_name="Начало (план)")
    end_planned = models.DateTimeField(verbose_name="Завершение (план)")
    start_actual = models.DateTimeField(null=True, blank=True, verbose_name="Начало (факт)")
    end_actual = models.DateTimeField(null=True, blank=True, verbose_name="Завершение (факт)")
    group_name = models.CharField(max_length=100, verbose_name="Название группы")
    is_group_success = models.BooleanField(default=False, verbose_name="Успех группы")
    group_notes = models.TextField(blank=True, verbose_name="Пояснение о группе (нештатные ситуации)")
    participants = models.ManyToManyField(Alpinist, through='Participation', related_name="climbs")

    def __str__(self):
        return f"{self.group_name} - {self.route.mountain.name}"

class Participation(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
        ('injury', 'Травма'),
        ('missing', 'Пропал без вести'),
        ('fatal', 'Летальный исход'),
        ('other', 'Другое'),
    ]
    alpinist = models.ForeignKey(Alpinist, on_delete=models.CASCADE, related_name="participations")
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE, related_name="details")
    is_success = models.BooleanField(default=False, verbose_name="Успех участника")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success', verbose_name="Состояние")
    incident_details = models.TextField(blank=True, verbose_name="Подробности нештатной ситуации")

    def __str__(self):
        return f"{self.alpinist.name} в {self.climb.group_name}"