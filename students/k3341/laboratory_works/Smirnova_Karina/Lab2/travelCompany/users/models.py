from django.contrib.auth.models import AbstractUser
from django.db import models

from students.k3341.laboratory_works.Smirnova_Karina.Lab2.travelCompany.main.models import Tour


class User(AbstractUser):
    reserved_tours = models.ManyToManyField(Tour, through='Reservation')

    def __str__(self):
        return self.username
