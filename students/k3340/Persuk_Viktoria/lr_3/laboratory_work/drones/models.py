from django.db import models


class Drones(models.Model):
    '''
    Модель для хранения данных о дронах
    '''
    # Choices

    CATEGORY_CHOICES = [
        ('hobby', 'Любительский'),
        ('commercial', 'Коммерческий'),
        ('pro', 'Профессиональный'),
    ]

    STATUS_CHOICES  = [
        ('active', 'Активен'),
        ('pending', 'Требуется проверка'),
        ('archived', 'Архивирован'),
    ]

    manufacturer = models.CharField(max_length=50, verbose_name='Производитель')
    model = models.CharField(max_length=50, verbose_name='Модель')
    serial_number = models.CharField(max_length=50, unique=True, verbose_name='Серийный номер')

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='commercial',
        verbose_name='Категория'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Статус'
    )

    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата регистрации дрона')
    weight = models.FloatField(null=True, blank=True, verbose_name='Вес')
    length = models.PositiveIntegerField(null=True, blank=True, verbose_name='Длина')
    width = models.PositiveIntegerField(null=True, blank=True, verbose_name='Ширина')
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name='Высока')
    max_speed = models.FloatField(null=True, blank=True, verbose_name='Максимальная скорость')
    max_flight_distance = models.FloatField(null=True, blank=True, verbose_name='Максимальная дистанция полёта')
    has_camera = models.BooleanField(verbose_name='Наличие камеры')


    def __str__(self):
        return f'{self.manufacturer} {self.model} {self.serial_number}'


class Flights(models.Model):
    '''
    Модель для хранения данных о полётах
    '''

    drone_id = models.ForeignKey(
        Drones,
        on_delete=models.CASCADE,
        related_name='flights',
        verbose_name='ID дрона'
    )

    start_datetime = models.DateTimeField(verbose_name='Дата и время начала полёта')
    end_datetime = models.DateTimeField(verbose_name='Дата и время конца полёта')
    location = models.CharField(max_length=50, verbose_name='Регион полёта')
    purpose = models.CharField(max_length=255, verbose_name='Причина полёта')
    distance = models.PositiveIntegerField(verbose_name='Дистанция в км')
    battery_usage = models.FloatField(verbose_name='Использованная батарея в %')
    notes = models.TextField(null=True, blank=True, verbose_name='Заметки')


    def __str__(self):
        return f'Полёт #{self.id} - дрон {self.drone_id.serial_number}'


class FlightLogs(models.Model):
    '''
    Модель для хранения логов полёта дрона
    '''

    flight_id = models.ForeignKey(
        Flights,
        on_delete=models.CASCADE,
        related_name='logs'
    )

    timestamp = models.DateTimeField(verbose_name='Дата и время лога')
    latitude = models.FloatField(verbose_name='Координаты высоты')
    longtitude = models.FloatField(verbose_name='Координаты ширины')
    altitude = models.FloatField(verbose_name='Высота полёта')
    battery = models.FloatField(verbose_name='Заряд батареи в %')
    message = models.TextField(null=True, blank=True, verbose_name='Сообщение')

    def __str__(self):
        return f'Лог {self.timestamp} для полёта {self.flight_id.id}'


class Documents(models.Model):
    '''
    Модель для хранения данных о документах
    '''

    # Choices
    DOCUMENT_TYPE_CHOICES = [
        ('certificate', 'Сертификат соответствия'),
        ('insurance', 'Страховой полис'),
        ('photo', 'Фото дрона'),
        ('license', 'Лицензия/разрешение'),
        ('other', 'Прочее'),
    ]

    drone_id = models.ForeignKey(
        Drones,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='ID дрона'
    )

    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name='Тип документа',
    )

    url = models.URLField(unique=True, verbose_name='URL файла')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время загрузки')


    def __str__(self):
        return f'{self.get_document_type_display} для дрона {self.drone_id.serial_number}'
