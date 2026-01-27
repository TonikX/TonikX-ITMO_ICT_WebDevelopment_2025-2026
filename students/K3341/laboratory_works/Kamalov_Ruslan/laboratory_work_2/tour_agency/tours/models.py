from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    name = models.CharField('Название', max_length=100)
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class TourAgency(models.Model):
    name = models.CharField('Название', max_length=200)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')

    class Meta:
        verbose_name = 'Турагентство'
        verbose_name_plural = 'Турагентства'

    def __str__(self):
        return self.name


class Tour(models.Model):
    name = models.CharField('Название тура', max_length=200)
    agency = models.ForeignKey(TourAgency, on_delete=models.CASCADE, verbose_name='Турагентство')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    description = models.TextField('Описание тура')
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    payment_conditions = models.TextField('Условия оплаты')

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    def __str__(self):
        return self.name


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур')
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    num_people = models.PositiveIntegerField('Количество человек', default=1)

    class Meta:
        verbose_name = 'Резервирование'
        verbose_name_plural = 'Резервирования'

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name='Тур')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tour_date_start = models.DateField('Дата начала тура')
    tour_date_end = models.DateField('Дата окончания тура')
    text = models.TextField('Комментарий')
    rating = models.PositiveIntegerField('Рейтинг', validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв от {self.user.username}"
