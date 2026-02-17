from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    EXPERIENCE_LEVELS = [
        ('beginner', 'Новичок'),
        ('amateur', 'Любитель'),
        ('professional', 'Профессионал'),
    ]

    experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVELS,
        default='beginner',
        verbose_name='Опыт'
    )
    driver_class = models.CharField(max_length=50, verbose_name='Класс гонщика', blank=True)
    team_name = models.CharField(max_length=100, verbose_name='Название команды', blank=True)
    car_description = models.TextField(verbose_name='Описание автомобиля', blank=True)
    driver_description = models.TextField(verbose_name='Описание гонщика', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
