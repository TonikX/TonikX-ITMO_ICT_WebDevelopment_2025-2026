from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = settings.AUTH_USER_MODEL

class Topic(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.city})" if self.city else self.name

class Conference(models.Model):
    title = models.CharField(max_length=200)
    topics = models.ManyToManyField(Topic, blank=True, related_name='conferences')
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='conferences')
    date_start = models.DateField()
    date_end = models.DateField()
    description = models.TextField(blank=True)
    participation_terms = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_start']

    def __str__(self):
        return self.title

class Registration(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Заявка отправлена'
        WITHDRAWN = 'withdrawn', 'Отозвана'

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='registrations')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')
    talk_title = models.CharField(max_length=200)
    talk_abstract = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)

    recommended_for_publication = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        unique_together = [('conference', 'author', 'talk_title')]

    def __str__(self):
        return f"{self.talk_title} — {self.author}"

class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    conf_date_start_snapshot = models.DateField()
    conf_date_end_snapshot = models.DateField()

    def save(self, *args, **kwargs):
        if not self.pk and self.conference_id:
            self.conf_date_start_snapshot = self.conference.date_start
            self.conf_date_end_snapshot = self.conference.date_end
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв {self.reviewer} → {self.conference} [{self.rating}]"
