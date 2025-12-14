from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Race(models.Model):
    """Модель автогонки"""
    name = models.CharField(max_length=200, verbose_name='Название гонки')
    date = models.DateField(verbose_name='Дата проведения')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    description = models.TextField(verbose_name='Описание гонки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Автогонка'
        verbose_name_plural = 'Автогонки'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.name} ({self.date})"


class Racer(models.Model):
    """Модель гонщика"""
    EXPERIENCE_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
        ('professional', 'Профессионал'),
    ]
    
    CLASS_CHOICES = [
        ('formula1', 'Формула-1'),
        ('formula2', 'Формула-2'),
        ('formula3', 'Формула-3'),
        ('rally', 'Ралли'),
        ('endurance', 'Выносливость'),
        ('other', 'Другое'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    team_name = models.CharField(max_length=200, verbose_name='Название команды')
    car_description = models.TextField(verbose_name='Описание автомобиля')
    racer_description = models.TextField(verbose_name='Описание участника')
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, verbose_name='Опыт')
    racer_class = models.CharField(max_length=20, choices=CLASS_CHOICES, verbose_name='Класс участника')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Гонщик'
        verbose_name_plural = 'Гонщики'
        ordering = ['full_name']
    
    def __str__(self):
        return self.full_name


class Registration(models.Model):
    """Модель регистрации гонщика на гонку"""
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE, verbose_name='Гонщик')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name='Гонка')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    race_time = models.TimeField(null=True, blank=True, verbose_name='Время заезда')
    result = models.CharField(max_length=100, blank=True, verbose_name='Результат')
    position = models.IntegerField(null=True, blank=True, verbose_name='Позиция')
    
    class Meta:
        verbose_name = 'Регистрация'
        verbose_name_plural = 'Регистрации'
        unique_together = ['racer', 'race']
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.racer.full_name} - {self.race.name}"


class Comment(models.Model):
    """Модель комментария к гонке"""
    COMMENT_TYPE_CHOICES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race_question', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]
    
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments', verbose_name='Гонка')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    race_date = models.DateField(verbose_name='Дата заезда')
    text = models.TextField(verbose_name='Текст комментария')
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPE_CHOICES, verbose_name='Тип комментария')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг (1-10)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Комментарий от {self.author.username} к {self.race.name}"
