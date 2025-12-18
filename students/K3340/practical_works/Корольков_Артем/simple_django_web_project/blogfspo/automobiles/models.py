# automobiles/models.py

from django.db import models


class Owner(models.Model):
    """
    Модель владельца автомобиля
    """
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name="Имя", null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", null=True, blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", null=True, blank=True)

    # Новые поля для владельца автомобиля
    passport_number = models.CharField(
        max_length=20,
        verbose_name="Номер паспорта",
        blank=True,
        #unique=True
    )

    address = models.TextField(
        verbose_name="Домашний адрес",
        blank=True,
        null=True,
        max_length=500
    )

    NATIONALITY_CHOICES = [
        ('RU', 'Российская Федерация'),
        ('BY', 'Республика Беларусь'),
        ('KZ', 'Республика Казахстан'),
        ('UA', 'Украина'),
        ('OTHER', 'Другая'),
    ]

    nationality = models.CharField(
        max_length=10,
        choices=NATIONALITY_CHOICES,
        verbose_name="Национальность",
        blank=True,
        null=True
    )

    # Связь многие-ко-многим с автомобилями через модель Ownership
    cars = models.ManyToManyField(
        'Car',
        through='Ownership',
        through_fields=('owner', 'car'),
        verbose_name="Автомобили",
        related_name='owners'  # Это позволит обращаться car.owners.all()
    )

    class Meta:
        db_table = 'owner'
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return f"Владелец {self.id}"

    def get_full_name(self):
        """Возвращает полное имя владельца"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return f"Владелец {self.id}"

    def get_nationality_display(self):
        """Возвращает отображаемое значение национальности"""
        if self.nationality:
            for code, name in self.NATIONALITY_CHOICES:
                if code == self.nationality:
                    return name
        return "Не указана"

    def get_short_address(self):
        """Возвращает сокращенный адрес (первые 50 символов)"""
        if self.address and len(self.address) > 50:
            return self.address[:50] + "..."
        return self.address


class Car(models.Model):
    """
    Модель автомобиля
    """
    id = models.AutoField(primary_key=True, verbose_name="ID автомобиля")
    state_number = models.IntegerField(verbose_name="Гос. удостоверение")
    brand = models.CharField(max_length=30, verbose_name="Марка")
    model = models.CharField(max_length=20, verbose_name="Модель")

    COLOR_CHOICES = [
        ('RED', 'Красный'),
        ('BLUE', 'Синий'),
        ('GREEN', 'Зеленый'),
        ('BLACK', 'Черный'),
        ('WHITE', 'Белый'),
        ('SILVER', 'Серебристый'),
        ('GRAY', 'Серый'),
        ('YELLOW', 'Желтый'),
        ('BROWN', 'Коричневый'),
    ]
    color = models.CharField(
        max_length=30,
        choices=COLOR_CHOICES,
        null=True,
        blank=True,
        verbose_name="Цвет"
    )

    class Meta:
        db_table = 'car'
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f"{self.brand} {self.model} ({self.state_number})"

    def get_current_owner(self):
        """Возвращает текущего владельца автомобиля"""
        # Исправлено: используем related_name 'ownerships'
        current_ownership = self.ownerships.filter(end_date__isnull=True).first()
        return current_ownership.owner if current_ownership else None

    def get_ownership_history(self):
        """Возвращает историю владения автомобилем"""
        return self.ownerships.all().order_by('-start_date')


class Ownership(models.Model):
    """
    Модель владения (ассоциативная сущность между владельцем и автомобилем)
    Содержит дополнительные атрибуты - даты начала и окончания владения
    """
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name='ownerships'  # Позволяет owner.ownerships.all()
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        verbose_name="Автомобиль",
        related_name='ownerships'  # Позволяет car.ownerships.all()
    )

    start_date = models.DateTimeField(verbose_name="Дата начала владения")
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата окончания владения"
    )

    class Meta:
        db_table = 'ownership'
        verbose_name = 'Владение'
        verbose_name_plural = 'Владения'
        # Уникальность комбинации владелец-автомобиль-период
        unique_together = ['owner', 'car', 'start_date']
        # Сортировка по дате начала владения (от новых к старым)
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.owner} - {self.car} ({self.start_date.date()})"

    def is_current(self):
        """Проверяет, является ли владение текущим"""
        return self.end_date is None


class DriverLicense(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID удостоверения")
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name='licenses'
    )
    license_number = models.CharField(
        max_length=10,
        verbose_name="Номер удостоверения"
    )

    LICENSE_TYPE_CHOICES = [
        ('A', 'Категория A - Мотоциклы'),
        ('B', 'Категория B - Легковые автомобили'),
        ('C', 'Категория C - Грузовые автомобили'),
        ('D', 'Категория D - Автобусы'),
        ('E', 'Категория E - Составы ТС'),
        ('BE', 'Категория BE - Легковые с прицепом'),
        ('CE', 'Категория CE - Грузовые с прицепом'),
        ('DE', 'Категория DE - Автобусы с прицепом'),
    ]
    license_type = models.CharField(
        max_length=10,
        choices=LICENSE_TYPE_CHOICES,
        verbose_name="Тип удостоверения"
    )

    issue_date = models.DateTimeField(verbose_name="Дата выдачи")
    expiry_date = models.DateTimeField(
        verbose_name="Дата окончания срока действия",
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'driver_license'
        verbose_name = 'Водительское удостоверение'
        verbose_name_plural = 'Водительские удостоверения'
        unique_together = ['license_number']

    def __str__(self):
        return f"Удостоверение {self.license_number} ({self.owner})"

    def is_valid(self):
        """Проверяет, действителен ли документ"""
        from django.utils import timezone
        if self.expiry_date:
            return timezone.now() <= self.expiry_date
        return True