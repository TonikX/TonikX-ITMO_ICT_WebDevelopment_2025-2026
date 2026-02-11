from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Conference(models.Model):
    title = models.CharField("Название", max_length=200)
    topics = models.TextField("Тематики")
    location = models.CharField("Место проведения", max_length=200)
    description = models.TextField("Описание")
    location_details = models.TextField("Как добраться")
    conditions = models.TextField("Условия участия")
    start_date = models.DateField("Начало")
    end_date = models.DateField("Конец")

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-start_date'] 


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Участник")
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, verbose_name="Конференция")
    talk_title = models.CharField("Тема доклада", max_length=255)
    

    is_recommended = models.BooleanField("Рекомендован к публикации", default=False)

    class Meta:
        unique_together = ('user', 'conference') 


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    text = models.TextField("Комментарий")
    rating = models.PositiveIntegerField("Рейтинг (1-10)", 
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']