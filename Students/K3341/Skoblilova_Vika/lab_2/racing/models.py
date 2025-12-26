"""
Модели приложения racing.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver


class Team(models.Model):
    """Команда автогонщиков."""
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class DriverProfile(models.Model):
    """Профиль водителя (гонщика), связан 1:1 с User."""
    
    DRIVER_CLASS_CHOICES = [
        ('A', 'Класс A'),
        ('B', 'Класс B'),
        ('C', 'Класс C'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='driver_profile',
        verbose_name='Пользователь'
    )
    full_name = models.CharField(max_length=200, verbose_name='Полное имя')
    car_description = models.CharField(max_length=300, blank=True, verbose_name='Описание автомобиля')
    bio = models.TextField(blank=True, verbose_name='Биография')
    experience_years = models.PositiveSmallIntegerField(default=0, verbose_name='Опыт (лет)')
    driver_class = models.CharField(
        max_length=1,
        choices=DRIVER_CLASS_CHOICES,
        default='C',
        verbose_name='Класс водителя'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='drivers',
        verbose_name='Команда'
    )

    class Meta:
        verbose_name = 'Профиль водителя'
        verbose_name_plural = 'Профили водителей'
        ordering = ['full_name']

    def __str__(self) -> str:
        return f"{self.full_name} ({self.user.username})"


@receiver(post_save, sender=User)
def create_or_update_driver_profile(sender, instance, created, **kwargs):
    """Автоматически создаем DriverProfile при создании User."""
    if created:
        DriverProfile.objects.create(
            user=instance,
            full_name=''  # Пользователь должен заполнить сам
        )


class Race(models.Model):
    """Автогонка (соревнование)."""
    title = models.CharField(max_length=200, verbose_name='Название')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    date = models.DateField(verbose_name='Дата')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Автогонка'
        verbose_name_plural = 'Автогонки'
        ordering = ['-date']

    def __str__(self) -> str:
        return f"{self.title} ({self.date})"


class Heat(models.Model):
    """Заезд в рамках гонки (например: Квалификация, Полуфинал, Финал)."""
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='heats',
        verbose_name='Гонка'
    )
    name = models.CharField(max_length=100, verbose_name='Название заезда', help_text='Например: Квалификация, Финал')
    start_time = models.DateTimeField(verbose_name='Время старта')
    laps = models.PositiveSmallIntegerField(default=1, verbose_name='Количество кругов')
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Запланирован'),
            ('in_progress', 'В процессе'),
            ('finished', 'Завершен'),
            ('cancelled', 'Отменен'),
        ],
        default='scheduled',
        verbose_name='Статус'
    )
    info = models.CharField(max_length=300, blank=True, verbose_name='Дополнительная информация')

    class Meta:
        verbose_name = 'Заезд'
        verbose_name_plural = 'Заезды'
        ordering = ['start_time']

    def __str__(self) -> str:
        return f"{self.name} - {self.race.title} ({self.start_time.strftime('%d.%m.%Y %H:%M')})"


class HeatResult(models.Model):
    """Результат водителя в конкретном заезде."""
    heat = models.ForeignKey(
        Heat,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Заезд'
    )
    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.CASCADE,
        related_name='heat_results',
        verbose_name='Водитель'
    )
    finish_time_seconds = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name='Время финиша (сек)',
        help_text='Время прохождения дистанции в секундах, например: 125.456'
    )
    position = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Позиция',
        help_text='Место в заезде (1, 2, 3...)'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('finished', 'Финишировал'),
            ('dnf', 'Не финишировал (DNF)'),
            ('dsq', 'Дисквалифицирован (DSQ)'),
            ('dns', 'Не стартовал (DNS)'),
        ],
        default='finished',
        verbose_name='Статус'
    )
    notes = models.CharField(max_length=300, blank=True, verbose_name='Примечания')

    class Meta:
        verbose_name = 'Результат заезда'
        verbose_name_plural = 'Результаты заездов'
        ordering = ['heat', 'position']
        constraints = [
            UniqueConstraint(
                fields=['heat', 'driver'],
                name='unique_heat_driver_result'
            )
        ]

    def __str__(self) -> str:
        pos = f"#{self.position}" if self.position else "—"
        return f"{pos} {self.driver.full_name} - {self.heat.name} ({self.finish_time_seconds}с)"
    
    def clean(self):
        """Валидация: водитель должен быть зарегистрирован на гонку."""
        from django.core.exceptions import ValidationError
        
        if self.heat and self.driver:
            # Проверяем, что водитель зарегистрирован на эту гонку
            is_registered = Registration.objects.filter(
                driver=self.driver,
                race=self.heat.race,
                active=True
            ).exists()
            
            if not is_registered:
                raise ValidationError(
                    f'Водитель {self.driver.full_name} не зарегистрирован на гонку "{self.heat.race.title}". '
                    f'Сначала зарегистрируйте водителя на гонку.'
                )
    
    def save(self, *args, **kwargs):
        """Переопределяем save для вызова clean()."""
        self.clean()
        super().save(*args, **kwargs)


class Registration(models.Model):
    """Регистрация водителя на гонку."""
    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Водитель'
    )
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Гонка'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    active = models.BooleanField(default=True, verbose_name='Активна')
    car_number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Номер машины',
        help_text='Гоночный номер для этой гонки'
    )

    class Meta:
        verbose_name = 'Регистрация'
        verbose_name_plural = 'Регистрации'
        ordering = ['-created_at']
        constraints = [
            UniqueConstraint(
                fields=['driver', 'race'],
                name='unique_driver_race_registration'
            )
        ]

    def __str__(self) -> str:
        return f"{self.driver.full_name} → {self.race.title}"


class Comment(models.Model):
    """Комментарий к гонке."""
    
    KIND_CHOICES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]
    
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Гонка'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    heat_date = models.DateField(verbose_name='Дата заезда')
    kind = models.CharField(
        max_length=20,
        choices=KIND_CHOICES,
        verbose_name='Тип комментария'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг',
        help_text='От 1 до 10'
    )
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Комментарий от {self.author.username} к {self.race.title}"

