from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
    )
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        # пример: ivanov (Студент)
        return f"{self.username} ({self.get_role_display()})"
