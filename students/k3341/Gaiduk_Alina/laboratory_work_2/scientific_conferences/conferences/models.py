from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:  # Метаданные модели
        ordering = ["name"] # Сортировка тем по имени по умолчанию

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "address")  # Чтобы не дублировать одну и ту же площадку

    def __str__(self):
        return self.name


class Conference(models.Model):
    title = models.CharField(max_length=200)
    topics = models.ManyToManyField(Topic)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    participation_terms = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-start_date"]  # Свежие мероприятия первыми

    def __str__(self):
        return self.title


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    presentation_title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)  # Краткое описание/тезисы
    created = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=50, choices=[
        ('pending', 'Ожидает'),
        ('recommended', 'Рекомендован к публикации'),
        ('not_recommended', 'Не рекомендован')
    ], default='pending')

    class Meta:
        # гарантия уникальности на уровне БД
        constraints = [
            models.UniqueConstraint(
                fields=["user", "conference"], name="uniq_user_conference_registration"
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.conference.title}'


class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conf_start_date = models.DateField()  # Дата начала
    conf_end_date = models.DateField()  # Дата окончания
    date_posted = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.PositiveIntegerField()

    class Meta:
        unique_together = ['conference', 'user']

    def __str__(self):
        return f'Отзыв от {self.user.username}'