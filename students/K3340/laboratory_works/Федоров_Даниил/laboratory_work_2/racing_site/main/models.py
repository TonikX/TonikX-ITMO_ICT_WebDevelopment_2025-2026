from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model



class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'

User = get_user_model()


class Race(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    has_occurred = models.BooleanField(default=False)

    def __str__(self):
        return f'Автогонка {self.name}'

class Racer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="racers")
    full_name = models.CharField(max_length=200)
    team_name = models.CharField(max_length=100)
    car_description = models.TextField()
    experience = models.IntegerField()
    racer_class = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'race')

    def __str__(self):
        return f'Участник {self.full_name} ({self.team_name})'


class Results(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="results")
    race_time = models.DurationField()
    winner = models.ForeignKey(Racer, on_delete=models.CASCADE, related_name="winner")

    def save(self, *args, **kwargs):
        if not self.race.has_occurred:
            self.race.has_occurred = True
            self.race.save()
        super(Results, self).save(*args, **kwargs)
    def __str__(self):
        return f'Результат гонки {self.race.name}, победитель: {self.winner.full_name}'


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    comment_type = models.CharField(max_length=100)
    rating = models.IntegerField()