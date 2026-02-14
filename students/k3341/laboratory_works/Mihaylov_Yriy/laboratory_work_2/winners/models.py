from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Racer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.CharField(max_length=100)
    car_description = models.TextField()
    racer_description = models.TextField()
    experience = models.IntegerField()
    classs = models.CharField()

    def __str__(self):
        return self.user.username


class Race(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    race_time = models.DateTimeField()

    def __str__(self):
        return self.name


class Commentator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class RaceRegistration(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['racer', 'race']


class Comment(models.Model):
    COMMENT_TYPES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('races', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    commentator = models.ForeignKey(Commentator, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    comment_type = models.CharField(max_length=30, choices=COMMENT_TYPES)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])

    def __str__(self):
        return f"Комментарий от {self.commentator.user.username}"


class Heat(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='heats')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    heat_time = models.DateTimeField()

    def __str__(self):
        return f"{self.race.name} - {self.name}"


class HeatResult(models.Model):
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE, related_name='results')
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    position = models.IntegerField()

    class Meta:
        unique_together = ['heat', 'racer']
        ordering = ['heat', 'position']

    def __str__(self):
        return f"{self.heat.name} - {self.racer.user.username} ({self.position} место)"

