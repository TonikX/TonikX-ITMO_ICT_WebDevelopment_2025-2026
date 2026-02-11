from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


# ===== МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ =====
class User(AbstractUser):
    """
    Кастомная модель пользователя с доп полями.
    Наследуемся от AbstractUser, чтобы не изобретать велосипед.
    """
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    home_address = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        """Строковое представление для админки и отладки"""
        return f"{self.username} ({self.first_name} {self.last_name})"


# ===== МОДЕЛЬ ГОНКИ =====
class Race(models.Model):
    """
    Модель гонки. Основная сущность приложения.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ===== МОДЕЛЬ ГОНЩИКА =====
class Racer(models.Model):
    """
    Регистрация пользователя на гонку.
    Связь ManyToMany через промежуточную модель.
    """
    # Опыт гонщика
    EXPERIENCE_CHOICES = [
        ('beginner', 'Начинающий'),
        ('amateur', 'Любитель'),
        ('professional', 'Профессионал'),
    ]

    # Связи
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='racers')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='racers')

    # Основная информация
    team_name = models.CharField(max_length=200)
    car_description = models.TextField()
    racer_description = models.TextField()
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    racer_class = models.CharField(max_length=50)

    # Статус и метаданные
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтверждено")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Один пользователь - одна регистрация на гонку
        unique_together = ('user', 'race')

    def __str__(self):
        return f"{self.user.username} - {self.race.name}"


# ===== МОДЕЛЬ РЕЗУЛЬТАТА =====
class RaceResult(models.Model):
    """
    Результаты заезда. Заполняется администратором.
    """
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE, related_name='results')
    race_time = models.TimeField()
    result = models.CharField(max_length=50)  # "1 место", "DNF", "DNS" и т.д.
    notes = models.TextField(blank=True, null=True)  # Дополнительные заметки
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.racer.user.username} - {self.result}"

    @property
    def experience_display(self):
        """Человекочитаемое отображение опыта"""
        return dict(self.EXPERIENCE_CHOICES).get(self.experience, self.experience)


# ===== МОДЕЛЬ КОММЕНТАРИЯ =====
class Comment(models.Model):
    """
    Комментарии пользователей к гонкам.
    """
    # Типы комментариев
    COMMENT_TYPES = [
        ('coop', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]

    # Связи
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    # Содержание
    text = models.TextField()
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.race.name}"
