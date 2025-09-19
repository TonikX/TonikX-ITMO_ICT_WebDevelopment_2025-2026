from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    reserved_tours = models.ManyToManyField('main.Tour', through='main.Reservation')

    def __str__(self):
        return self.username
