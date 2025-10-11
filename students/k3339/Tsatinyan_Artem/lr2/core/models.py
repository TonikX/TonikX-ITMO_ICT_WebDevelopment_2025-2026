from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Conference(models.Model):
    title = models.CharField(max_length=255)
    topics = models.ManyToManyField(Topic, blank=True, related_name='conferences')
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='conferences')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    participation_terms = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('conference_detail', args=[self.pk])

class Registration(models.Model):
    """Заявка автора на выступление (CRUD доступен только владельцу)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='registrations')
    talk_title = models.CharField(max_length=255)
    talk_abstract = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Итог для админа: рекомендовано к публикации или нет
    recommended_to_publish = models.BooleanField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'conference') # один доклад на пользователя/конфу
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} → {self.conference}: {self.talk_title}"

    def get_absolute_url(self):
        return self.conference.get_absolute_url()

class Review(models.Model):
    """Отзыв к конференции. Снимок дат конференции сохраняется при создании."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveSmallIntegerField() # 1..10
    created_at = models.DateTimeField(auto_now_add=True)

    # Снимок дат
    conference_start_snapshot = models.DateField()
    conference_end_snapshot = models.DateField()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk: # при первом сохранении фиксируем даты
            self.conference_start_snapshot = self.conference.start_date
            self.conference_end_snapshot = self.conference.end_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.conference} · {self.user} · {self.rating}"