from django.contrib.auth.models import AbstractUser
from django.db import models

class AdminUser(AbstractUser):
    """ Сотрудник """
    phone = models.CharField("Телефон", max_length=50, blank=True)
    position = models.CharField("Должность", max_length=100, blank=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.username


class Client(models.Model):
    """Компания / юридическое лицо — клиент"""
    company_name = models.CharField("Название компании", max_length=255)
    inn = models.CharField("ИНН", max_length=50, blank=True)
    email = models.EmailField("Электронная почта", blank=True, null=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    contact_person = models.CharField("Контактное лицо", max_length=255, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.company_name


class Car(models.Model):
    """Автомобиль"""
    STATUS_CHOICES = [
        ("available", "Доступен"),
        ("leased", "В аренде"),
        ("maintenance", "На обслуживании"),
        ("sold", "Продан"),
    ]

    vin = models.CharField("VIN", max_length=50, unique=True)
    make = models.CharField("Марка", max_length=100)
    model = models.CharField("Модель", max_length=100)
    year = models.PositiveSmallIntegerField("Год выпуска", null=True, blank=True)
    license_plate = models.CharField("Гос. номер", max_length=20, unique=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="available")
    current_mileage = models.PositiveIntegerField("Текущий пробег (км)", null=True, blank=True)
    purchase_date = models.DateField("Дата покупки", null=True, blank=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class Lease(models.Model):
    """Договор аренды"""
    STATUS_CHOICES = [
        ("active", "Активный"),
        ("completed", "Завершён"),
        ("cancelled", "Отменён"),
    ]

    car = models.ForeignKey(Car, verbose_name="Автомобиль", related_name="leases", on_delete=models.PROTECT)
    client = models.ForeignKey(Client, verbose_name="Клиент", related_name="leases", on_delete=models.PROTECT)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания", null=True, blank=True)
    monthly_payment = models.DecimalField("Ежемесячная оплата", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="active")
    created_by_admin = models.ForeignKey(AdminUser, verbose_name="Создал сотрудник", related_name="created_leases", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Договор аренды"
        verbose_name_plural = "Договоры аренды"

    def __str__(self):
        return f"Договор #{self.pk} — {self.car} / {self.client}"


class LeaseApplication(models.Model):
    """ заявка на аренду авто """

    car = models.ForeignKey(Car, verbose_name="Автомобиль", related_name="lease_applications", on_delete=models.PROTECT)
    client = models.ForeignKey(Client, verbose_name='Клиент', related_name="lease_applications", on_delete=models.PROTECT)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

class MaintenanceCompany(models.Model):
    """Компания, проводящая обслуживание"""
    name = models.CharField("Название компании", max_length=255)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Компания сервиса"
        verbose_name_plural = "Компании сервиса"

    def __str__(self):
        return self.name

class Maintenance(models.Model):
    """Сведения об обслуживании авто"""
    car = models.ForeignKey(Car, verbose_name="Автомобиль", related_name="maintenances", on_delete=models.CASCADE)
    maintenance_company = models.ForeignKey(MaintenanceCompany, verbose_name='Сервис', related_name="maintenances", on_delete=models.PROTECT)
    date = models.DateField("Дата обслуживания")
    service = models.CharField("Вид обслуживания", max_length=255)
    cost = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, null=False, blank=True)
    description = models.TextField("Описание", blank=True)
    created_by_admin = models.ForeignKey(AdminUser, verbose_name="Записал сотрудник", related_name="created_maintenances", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("Дата записи", auto_now_add=True)

    class Meta:
        verbose_name = "Обслуживание"
        verbose_name_plural = "Обслуживания"

    def __str__(self):
        return f"{self.car} — {self.service} ({self.date})"


class CarSpecification(models.Model):
    """Характеристики автомобиля (одна запись на автомобиль)"""
    ENGINE_TYPE_CHOICES = [
        ("petrol", "Бензин"),
        ("diesel", "Дизель"),
        ("electric", "Электро"),
        ("hybrid", "Гибрид"),
        ("other", "Другое"),
    ]

    TRANSMISSION_CHOICES = [
        ("auto", "Автомат"),
        ("manual", "Механика"),
        ("cvt", "Вариатор"),
        ("robot", "Робот"),
    ]

    DRIVETRAIN_CHOICES = [
        ("fwd", "Передний"),
        ("rwd", "Задний"),
        ("awd", "Полный"),
    ]

    BODY_TYPE_CHOICES = [
        ("sedan", "Седан"),
        ("hatchback", "Хэтчбек"),
        ("suv", "SUV"),
        ("wagon", "Универсал"),
        ("van", "Фургон"),
        ("coupe", "Купе"),
        ("other", "Другое"),
    ]

    car = models.OneToOneField(Car, verbose_name="Автомобиль", related_name="specification", on_delete=models.CASCADE)
    engine_type = models.CharField("Тип двигателя", max_length=20, choices=ENGINE_TYPE_CHOICES, default="petrol")
    engine_volume = models.DecimalField("Объём двигателя (л)", max_digits=4, decimal_places=2, null=True, blank=True)
    horsepower = models.PositiveIntegerField("Мощность (л.с.)", null=True, blank=True)
    transmission = models.CharField("Коробка передач", max_length=20, choices=TRANSMISSION_CHOICES, blank=True)
    drivetrain = models.CharField("Привод", max_length=10, choices=DRIVETRAIN_CHOICES, blank=True)
    body_type = models.CharField("Тип кузова", max_length=20, choices=BODY_TYPE_CHOICES, blank=True)
    fuel_consumption = models.DecimalField("Расход топлива (л/100км)", max_digits=5, decimal_places=2, null=True, blank=True)
    color = models.CharField("Цвет", max_length=50, blank=True)
    additional_options = models.TextField("Дополнительные опции", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Характеристики автомобиля"
        verbose_name_plural = "Характеристики автомобилей"

    def __str__(self):
        return f"Характеристики {self.car}"


class Fleet(models.Model):
    """Автопарк / филиал"""
    name = models.CharField("Название автопарка", max_length=255)
    address = models.CharField("Адрес автопарка", max_length=255, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Автопарк"
        verbose_name_plural = "Автопарки"

    def __str__(self):
        return self.name


class CarFleet(models.Model):
    """Принадлежность машины к автопарку (по одному автопарку на машину)"""
    car = models.OneToOneField(Car, verbose_name="Автомобиль", related_name="car_fleet", on_delete=models.CASCADE)
    fleet = models.ForeignKey(Fleet, verbose_name="Автопарк", related_name="cars", on_delete=models.CASCADE)
    assigned_at = models.DateField("Дата прикрепления", null=True, blank=True)

    class Meta:
        verbose_name = "Принадлежность к автопарку"
        verbose_name_plural = "Принадлежность к автопаркам"

    def __str__(self):
        return f"{self.car} → {self.fleet}"




