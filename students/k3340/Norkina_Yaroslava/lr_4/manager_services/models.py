from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Пользователь системы"""

    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(verbose_name='username', max_length=20, unique=True)
    email = models.EmailField('Электронная почта', unique=True)
    phone = models.CharField('Номер телефона', max_length=20, blank=True)
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN


class Service(models.Model):
    """Услуга"""

    name = models.CharField('Название услуги', max_length=200)
    description = models.TextField('Описание услуги')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField('Продолжительность (в минутах)')
    category = models.CharField('Категория', max_length=100)
    is_active = models.BooleanField('Активна', default=True)
    created_by = models.ForeignKey(
        User,
        verbose_name='Кто создал',
        on_delete=models.PROTECT,
        related_name='created_services',
        limit_choices_to={'role': User.Role.ADMIN}
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Order(models.Model):
    """Заявка на услугу"""

    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        COMPLETED = 'completed', 'Завершена'
        CANCELLED = 'cancelled', 'Отменена'

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    service = models.ForeignKey(
        Service,
        verbose_name='Услуга',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    notes = models.TextField('Дополнительные заметки', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    completed_at = models.DateTimeField('Дата завершения', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка #{self.id} - {self.user.email}'

    def save(self, *args, **kwargs):
        # Автоматически устанавливаем completed_at при завершении заявки
        if self.status == self.Status.COMPLETED and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        elif self.status != self.Status.COMPLETED:
            self.completed_at = None
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """История изменения статусов заявки"""

    order = models.ForeignKey(
        Order,
        verbose_name='Заявка',
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    old_status = models.CharField('Старый статус', max_length=20, choices=Order.Status.choices)
    new_status = models.CharField('Новый статус', max_length=20, choices=Order.Status.choices)
    changed_by = models.ForeignKey(
        User,
        verbose_name='Кто изменил',
        on_delete=models.PROTECT,
        related_name='changed_statuses',
        limit_choices_to={'role': User.Role.ADMIN}
    )
    changed_at = models.DateTimeField('Дата изменения', auto_now_add=True)
    comment = models.TextField('Комментарий к изменению', blank=True)

    class Meta:
        verbose_name = 'История статуса'
        verbose_name_plural = 'История статусов'
        ordering = ['-changed_at']

    def __str__(self):
        return f'{self.order} - {self.old_status} → {self.new_status}'


class Comment(models.Model):
    """Комментарий к заявке"""

    order = models.ForeignKey(
        Order,
        verbose_name='Заявка',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    admin = models.ForeignKey(
        User,
        verbose_name='Администратор',
        on_delete=models.PROTECT,
        related_name='comments',
        limit_choices_to={'role': User.Role.ADMIN}
    )
    content = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_visible_to_user = models.BooleanField('Виден пользователю', default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий к заявке #{self.order.id}'


class File(models.Model):
    """Файл/Изображение для услуги"""

    service = models.ForeignKey(
        Service,
        verbose_name='Услуга',
        on_delete=models.CASCADE,
        related_name='files'
    )
    file_name = models.CharField('Оригинальное имя файла', max_length=255)
    file_path = models.CharField('Путь к файлу', max_length=500)
    file_size = models.PositiveIntegerField('Размер файла (в байтах)')
    mime_type = models.CharField('Тип файла', max_length=100)
    is_primary = models.BooleanField('Главное изображение', default=False)
    display_order = models.PositiveIntegerField('Порядок отображения', default=0)
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User,
        verbose_name='Кто загрузил',
        on_delete=models.PROTECT,
        related_name='uploaded_files',
        limit_choices_to={'role': User.Role.ADMIN}
    )
    alt_text = models.CharField('Альтернативный текст', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['display_order', 'uploaded_at']

    def __str__(self):
        return self.file_name


class Review(models.Model):
    """Отзыв на услугу"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    service = models.ForeignKey(
        Service,
        verbose_name='Услуга',
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    order = models.ForeignKey(
        Order,
        verbose_name='Заявка',
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст отзыва')
    is_verified = models.BooleanField('Подтвержден', default=True)
    is_published = models.BooleanField('Опубликован', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['order'],
                name='unique_review_per_order'
            )
        ]

    def __str__(self):
        return f'Отзыв от {self.user.email} на {self.service.name}'