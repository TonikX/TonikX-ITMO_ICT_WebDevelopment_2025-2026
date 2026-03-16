from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):

    RACER_CHOICES = [
        ('A', 'Класс A'),
        ('B', 'Класс B'),
        ('C', 'Класс C'),
    ]

    bio = models.TextField(blank=True, null=True, verbose_name="Описание участника")
    experience = models.IntegerField(default=0, verbose_name="Опыт (лет)")
    racer_class = models.CharField(
            max_length=10, 
            choices=RACER_CHOICES, 
            default='C', 
            verbose_name="Класс"
        )
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}" if self.first_name else self.username 

class Race(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название гонки")
    date = models.DateTimeField(verbose_name="Дата и время заезда")
    location = models.CharField(max_length=255, verbose_name="Место проведения")

    def __str__(self):
        return self.title

class Registration(models.Model):
    """Связь гонщика и гонки (Many-to-Many с доп. полями)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Гонщик")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name="Гонка")
    car_description = models.CharField(max_length=255, verbose_name="Описание автомобиля")
    team_name = models.CharField(max_length=100, verbose_name="Название команды")
    
    # заполняется админом
    race_time = models.DurationField(null=True, blank=True, verbose_name="Время заезда")
    result_place = models.PositiveIntegerField(null=True, blank=True, verbose_name="Место")

    class Meta:
        unique_together = ('user', 'race') # один гонщик - одна регистрация на гонку

class Comment(models.Model):
    TYPE_CHOICES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Комментарий")
    comment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='race')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)], verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True)