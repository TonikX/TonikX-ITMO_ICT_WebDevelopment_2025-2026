# carshering/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator

# ========================
# 1. Расширенный пользователь (Users → User)
# ========================
class User(AbstractUser):
    # Поле user_name из SQL заменяется на first_name + last_name или username
    # Но если нужно именно user_name — добавим его
    user_name = models.CharField("Имя пользователя", max_length=50)

    def __str__(self):
        return self.user_name or self.username


# ========================
# 2. Models → Model
# ========================
# models.py
from django.db import models
from django.core.validators import MinLengthValidator

class Model(models.Model):
    brand = models.CharField(
        "Марка",
        max_length=50,
        validators=[MinLengthValidator(1, "Марка не может быть пустой")]
    )
    model_name = models.CharField(
        "Модель",
        max_length=50,
        validators=[MinLengthValidator(1, "Модель не может быть пустой")]
    )
    power = models.PositiveIntegerField("Мощность (л.с.)")

    class Meta:
        verbose_name = "Модель автомобиля"
        verbose_name_plural = "Модели автомобилей"

    def __str__(self):
        return f"{self.brand} {self.model_name}"


# ========================
# 3. Cars → Car
# ========================
class Car(models.Model):
    mileage = models.PositiveIntegerField("Пробег", default=0)
    licence = models.CharField(
        "Гос. номер",
        max_length=9,
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]{1,9}$', 'Номер должен содержать до 9 латинских букв и цифр')]
    )
    serial_number = models.CharField("VIN", max_length=17, blank=True)
    buying_date = models.DateField("Дата покупки")
    city = models.CharField("Город", max_length=50, blank=True)
    coordinates = models.FloatField("Координаты")
    malfunctions = models.TextField("Неисправности", blank=True)
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        verbose_name="Модель",
        related_name='cars'
    )

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.licence} ({self.model})"


# ========================
# 4. Passport
# ========================
class Passport(models.Model):
    passport_number = models.CharField(
        "Номер паспорта",
        max_length=6,
        unique=True,
        validators=[RegexValidator(r'^\d{6}$', 'Номер паспорта — 6 цифр')]
    )
    serial_number = models.CharField(
        "Серия паспорта",
        max_length=4,
        validators=[RegexValidator(r'^\d{4}$', 'Серия паспорта — 4 цифры')]
    )
    birth_date = models.DateField("Дата рождения")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='passport'
    )

    class Meta:
        verbose_name = "Паспорт"
        verbose_name_plural = "Паспорта"

    def __str__(self):
        return f"Паспорт {self.serial_number} {self.passport_number}"


# ========================
# 5. DriverLicense
# ========================
class DriverLicense(models.Model):
    date_of_issue = models.DateField("Дата выдачи")
    expiration_date = models.DateField("Срок действия")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Водитель",
        related_name='driver_license'
    )

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"

    def __str__(self):
        return f"ВУ {self.user.user_name} (до {self.expiration_date})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.expiration_date <= self.date_of_issue:
            raise ValidationError("Срок действия должен быть позже даты выдачи.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# ========================
# 6. Repairs
# ========================
class Repair(models.Model):
    description = models.TextField("Описание", blank=True)
    datetime = models.DateTimeField("Дата и время ремонта")
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        verbose_name="Автомобиль",
        related_name='repairs'
    )

    class Meta:
        verbose_name = "Ремонт"
        verbose_name_plural = "Ремонты"

    def __str__(self):
        return f"Ремонт {self.car.licence} от {self.datetime.date()}"


# ========================
# 7. Payment
# ========================
class Payment(models.Model):
    description = models.TextField("Описание")
    value = models.FloatField(
        "Сумма",
        validators=[MinValueValidator(0.01, "Сумма должна быть положительной")]
    )
    date = models.DateField("Дата платежа")
    deadline = models.DateField("Срок оплаты")
    type = models.CharField("Тип платежа", max_length=50, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='payments'
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платёж {self.user.user_name}: {self.value} руб."

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.deadline <= self.date:
            raise ValidationError("Срок оплаты должен быть позже даты платежа.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# ========================
# 8. Tariffs
# ========================
class Tariff(models.Model):
    price_per_minute = models.PositiveIntegerField("Цена за минуту", null=True, blank=True)
    start_time = models.DateTimeField("Начало действия")
    end_time = models.DateTimeField("Окончание действия")
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        verbose_name="Модель",
        related_name='tariffs'
    )

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return f"Тариф для {self.model} ({self.start_time} – {self.end_time})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_time <= self.start_time:
            raise ValidationError("Окончание должно быть позже начала.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# ========================
# 9. Trip
# ========================
class Trip(models.Model):
    start_time = models.DateTimeField("Начало поездки")
    end_time = models.DateTimeField("Окончание поездки")
    problems = models.TextField("Проблемы", blank=True)
    comments = models.TextField("Комментарии", blank=True)
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        verbose_name="Автомобиль",
        related_name='trips'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='trips'
    )

    class Meta:
        verbose_name = "Поездка"
        verbose_name_plural = "Поездки"

    def __str__(self):
        return f"Поездка {self.user.user_name} на {self.car.licence}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_time <= self.start_time:
            raise ValidationError("Окончание поездки должно быть позже начала.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)