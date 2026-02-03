from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta


class Hotel(models.Model):
    """Модель отеля"""
    name = models.CharField(max_length=200, verbose_name='Название отеля')
    owner = models.CharField(max_length=200, verbose_name='Владелец')
    address = models.TextField(verbose_name='Адрес')
    description = models.TextField(verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
    
    def __str__(self):
        return self.name


class RoomType(models.Model):
    """Модель типа номера"""
    AMENITIES_CHOICES = [
        ('wifi', 'WiFi'),
        ('tv', 'Телевизор'),
        ('minibar', 'Мини-бар'),
        ('conditioner', 'Кондиционер'),
        ('safe', 'Сейф'),
        ('bathroom', 'Ванная комната'),
        ('balcony', 'Балкон'),
    ]
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types', verbose_name='Отель')
    name = models.CharField(max_length=100, verbose_name='Тип номера')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость за сутки')
    capacity = models.IntegerField(verbose_name='Вместимость (человек)')
    amenities = models.JSONField(default=list, verbose_name='Удобства')
    available_count = models.IntegerField(default=1, verbose_name='Количество доступных номеров')
    
    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'
    
    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class Reservation(models.Model):
    """Модель резервирования"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('checked_in', 'Заселен'),
        ('checked_out', 'Выселен'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name='Пользователь')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='reservations', verbose_name='Тип номера')
    check_in_date = models.DateField(verbose_name='Дата заезда')
    check_out_date = models.DateField(verbose_name='Дата выезда')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Резервирование'
        verbose_name_plural = 'Резервирования'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.room_type.name} ({self.check_in_date} - {self.check_out_date})"
    
    @property
    def total_price(self):
        """Рассчитывает общую стоимость проживания"""
        days = (self.check_out_date - self.check_in_date).days
        return self.room_type.price * days
    
    @classmethod
    def get_recent_guests(cls, hotel_id=None):
        """Возвращает список постояльцев за последний месяц"""
        one_month_ago = datetime.now().date() - timedelta(days=30)
        query = cls.objects.filter(
            status__in=['checked_in', 'checked_out'],
            check_in_date__gte=one_month_ago
        ).select_related('user', 'room_type__hotel')
        
        if hotel_id:
            query = query.filter(room_type__hotel_id=hotel_id)
        
        return query.order_by('-check_in_date')


class Review(models.Model):
    """Модель отзыва"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='reviews', verbose_name='Тип номера')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews', verbose_name='Резервирование')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг (1-10)'
    )
    comment = models.TextField(verbose_name='Комментарий')
    stay_period_start = models.DateField(verbose_name='Начало периода проживания')
    stay_period_end = models.DateField(verbose_name='Конец периода проживания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.room_type.name} (рейтинг: {self.rating}/10)"
