from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с ролью
    """
    ROLE_CHOICES = [
        ('resident', 'Жилец'),
        ('master', 'Мастер'),
        ('dispatcher', 'Диспетчер'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='resident',
        verbose_name='Роль'
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер телефона'
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Адрес проживания'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Building(models.Model):
    """
    Модель жилого дома
    """
    address = models.CharField(max_length=255, verbose_name="Адрес дома")
    total_floors = models.PositiveIntegerField(verbose_name="Количество этажей")
    year_built = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Год постройки"
    )
    total_apartments = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Количество квартир"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"
        ordering = ['address']
    
    def __str__(self):
        return self.address


class Apartment(models.Model):
    """
    Модель квартиры
    """
    ROOM_CHOICES = [
        (1, '1 комната'),
        (2, '2 комнаты'),
        (3, '3 комнаты'),
        (4, '4 комнаты'),
        (5, '5+ комнат'),
    ]
    
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='apartments',
        verbose_name="Дом"
    )
    number = models.CharField(max_length=10, verbose_name="Номер квартиры")
    floor = models.PositiveIntegerField(verbose_name="Этаж")
    area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Площадь (кв.м)")
    rooms = models.PositiveIntegerField(
        choices=ROOM_CHOICES,
        null=True,
        blank=True,
        verbose_name="Количество комнат"
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Баланс счета"
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='apartments',
        verbose_name="Владелец"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"
        ordering = ['building', 'number']
        unique_together = [['building', 'number']]
    
    def __str__(self):
        return f"Кв. {self.number}, {self.building.address}"


class ServiceCategory(models.Model):
    """
    Справочник категорий заявок
    """
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    """
    Модель заявки на обслуживание
    """
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнено'),
        ('canceled', 'Отменена'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('urgent', 'Срочный'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Тема обращения")
    description = models.TextField(verbose_name="Описание проблемы")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="Приоритет"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    assigned_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата назначения мастера"
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата начала работы"
    )
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата решения")
    worker_comment = models.TextField(blank=True, null=True, verbose_name="Комментарий мастера")
    
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requests',
        verbose_name="Категория"
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='requests',
        verbose_name="Квартира"
    )
    requester = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='created_requests',
        verbose_name="Заявитель"
    )
    worker = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests',
        verbose_name="Мастер-исполнитель"
    )
    
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заявка #{self.id} - {self.title}"


class MeterReading(models.Model):
    """
    Модель показаний счетчиков
    """
    METER_TYPES = [
        ('hot_water', 'Горячая вода'),
        ('cold_water', 'Холодная вода'),
        ('electricity', 'Электричество'),
        ('gas', 'Газ'),
    ]
    
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='readings',
        verbose_name="Квартира"
    )
    meter_type = models.CharField(
        max_length=20,
        choices=METER_TYPES,
        verbose_name="Тип счетчика"
    )
    value = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Показания")
    previous_value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Предыдущее показание"
    )
    consumption = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Расход"
    )
    date_recorded = models.DateField(auto_now_add=True, verbose_name="Дата подачи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Показание счетчика"
        verbose_name_plural = "Показания счетчиков"
        ordering = ['-date_recorded', '-created_at']
    
    def __str__(self):
        return f"{self.get_meter_type_display()}: {self.value} (Кв. {self.apartment.number})"

