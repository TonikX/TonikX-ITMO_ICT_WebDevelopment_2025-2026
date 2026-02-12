from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

COMMENT_TYPES = [
    ('coop', 'Вопрос о сотрудничестве'),
    ('race', 'Вопрос о гонках'),
    ('other', 'Иное'),
]

CLASS_CHOICES = [
    ('A','Класс A'),
    ('B','Класс B'),
    ('C','Класс C'),
]


class ParticipantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField("ФИО", max_length=200)
    team_name = models.CharField("Название команды", max_length=200, blank=True)
    description = models.TextField("Описание участника", blank=True)
    experience_years = models.PositiveIntegerField("Опыт (лет)", default=0)
    participant_class = models.CharField("Класс участника", max_length=2, choices=CLASS_CHOICES, default='C')

    def __str__(self):
        return self.full_name or self.user.username


class Car(models.Model):
    owner = models.ForeignKey(ParticipantProfile, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField("Название автомобиля", max_length=200)
    description = models.TextField("Описание автомобиля", blank=True)

    def __str__(self):
        return f"{self.name} ({self.owner})"


class Race(models.Model):
    title = models.CharField("Название гонки", max_length=200)
    date = models.DateTimeField("Дата гонки", null=True, blank=True)
    location = models.CharField("Место", max_length=200, blank=True)
    description = models.TextField("Описание гонки", blank=True)

    def __str__(self):
        return f"{self.title} — {self.date.date() if self.date else 'дата не указана'}"


class Registration(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registrations')
    participant = models.ForeignKey(ParticipantProfile, on_delete=models.CASCADE, related_name='registrations')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    finish_time_ms = models.BigIntegerField("Время заезда (мс)", null=True, blank=True)
    position = models.PositiveIntegerField("Позиция (место)", null=True, blank=True)

    class Meta:
        unique_together = ('race', 'participant')  # один участник — одна регистрация на гонку

    def __str__(self):
        return f"{self.participant} @ {self.race.title}"


class Comment(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments')
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='race_comments')
    text = models.TextField("Текст комментария")
    comment_type = models.CharField("Тип комментария", max_length=10, choices=COMMENT_TYPES)
    rating = models.PositiveSmallIntegerField("Рейтинг (1-10)", default=5)
    created_at = models.DateTimeField("Дата комментария", default=timezone.now)

    def save(self, *args, **kwargs):
        if self.rating < 1:
            self.rating = 1
        if self.rating > 10:
            self.rating = 10
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Комментарий от {self.commentator} к {self.race}"
