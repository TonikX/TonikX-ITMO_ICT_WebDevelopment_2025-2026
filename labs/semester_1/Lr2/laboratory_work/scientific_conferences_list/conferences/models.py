from django.db import models
from users.models import User


class Conference(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    topics = models.CharField(max_length=255, blank=True)
    participation_conditions = models.TextField(blank=True)
    venue_name = models.CharField(max_length=255)
    venue_description = models.TextField(blank=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f'{self.name} ({self.start_date} - {self.end_date})'


class Presentation(models.Model):
    RECOMMENDATION_CHOICES = [
        (None, "Не оценено"),
        (True, "Рекомендован"),
        (False, "Не рекомендован"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    recommendation = models.BooleanField(choices=RECOMMENDATION_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.title} | {self.author}"


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f"Отзыв #{self.pk} - {self.rating}"
