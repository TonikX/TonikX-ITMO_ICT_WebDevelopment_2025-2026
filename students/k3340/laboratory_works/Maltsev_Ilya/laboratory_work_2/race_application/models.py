from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
    has_racer = models.BooleanField(default=False)


class Racer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    car_description = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    experience = models.IntegerField()
    racer_class = models.CharField(max_length=100)


class Race(models.Model):
    race_statuses = (
        ('r', 'registration'),
        ('i', 'in progress'),
        ('e', 'ended')
    )
    date_of_race = models.DateField(name='date_of_race')
    status = models.CharField(choices=race_statuses, max_length=1)
    winner = models.ForeignKey(Racer, blank=True, null=True, on_delete=models.SET_NULL)


class RaceConnection(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)


class Review(models.Model):
    review_types = (
        ('p', 'partnership'),
        ('r', 'race'),
        ('o', 'other')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    type = models.CharField(choices=review_types, max_length=1)
    review = models.CharField(max_length=1000)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])