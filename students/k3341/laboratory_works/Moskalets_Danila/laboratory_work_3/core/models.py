from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User с email вместо username"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Создает и сохраняет пользователя с email и паролем"""
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Создает обычного пользователя"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Создает суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('Email', unique=True)

    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.name} {self.surname})"


class SecurityCompany(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='security_companies',
        verbose_name='Владелец/администратор'
    )
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    logo = models.CharField('Логотип', max_length=500, blank=True, null=True)
    website = models.URLField('Веб-сайт', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Охранная компания'
        verbose_name_plural = 'Охранные компании'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        from django.db.models import Avg
        result = self.reviews.aggregate(Avg('rating'))
        return result['rating__avg'] or 0


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    security_company = models.ForeignKey(
        SecurityCompany,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Охранная компания'
    )
    name = models.CharField('Название услуги', max_length=200)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(
        Category,
        through='ServiceCategory',
        related_name='services',
        verbose_name='Категории'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']
        unique_together = ['security_company', 'name']

    def __str__(self):
        return f"{self.name} ({self.security_company.name})"

    @property
    def current_price(self):
        from django.utils import timezone
        now = timezone.now()

        active_discount = self.discounts.filter(
            start_date__lte=now,
            end_date__gte=now
        ).first()

        if active_discount:
            return self.price * (1 - active_discount.discount_percent / 100)
        return self.price


class ServiceCategory(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуга'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'
        unique_together = ['service', 'category']

    def __str__(self):
        return f"{self.service.name} - {self.category.name}"


class ServiceDiscount(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='discounts',
        verbose_name='Услуга'
    )
    discount_percent = models.DecimalField(
        'Процент скидки',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Скидка на услугу'
        verbose_name_plural = 'Скидки на услуги'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.discount_percent}% скидка на {self.service.name}"

    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='service_requests',
        verbose_name='Пользователь'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='requests',
        verbose_name='Услуга'
    )
    description = models.TextField('Описание заявки')
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    admin_comment = models.TextField('Комментарий администратора', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заявка на услугу'
        verbose_name_plural = 'Заявки на услуги'
        ordering = ['-created_at']

    def __str__(self):
        status_display = dict(self.STATUS_CHOICES).get(self.status, self.status)
        return f"Заявка #{self.id} - {self.service.name} ({status_display})"


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    security_company = models.ForeignKey(
        SecurityCompany,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Охранная компания'
    )
    rating = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField('Комментарий', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['user', 'security_company']

    def __str__(self):
        return f"Отзыв от {self.user.email} для {self.security_company.name}"


class UserFavorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Услуга'
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Избранная услуга'
        verbose_name_plural = 'Избранные услуги'
        ordering = ['-created_at']
        unique_together = ['user', 'service']

    def __str__(self):
        return f"{self.user.email} - {self.service.name}"