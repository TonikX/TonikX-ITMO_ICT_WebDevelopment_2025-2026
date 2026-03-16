from django.db import models
from django.conf import settings
from django.urls import reverse


class Race(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название гонки')
    description = models.TextField(verbose_name='Описание гонки')
    date = models.DateTimeField(verbose_name='Дата проведения')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('race_detail', kwargs={'race_id': self.id})

    def get_registered_users_count(self):
        return self.raceregistration_set.filter(is_confirmed=True).count()

    def get_comments_count(self):
        return self.comment_set.count()

    class Meta:
        verbose_name = 'Гонка'
        verbose_name_plural = 'Гонки'
        ordering = ['-date']


class RaceRegistration(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name='Гонка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Участник')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False, verbose_name='Подтверждена')

    class Meta:
        unique_together = ['race', 'user']
        verbose_name = 'Регистрация на гонку'
        verbose_name_plural = 'Регистрации на гонки'

    def __str__(self):
        return f"{self.user} - {self.race}"


class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name='Гонка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Участник')
    lap_time = models.DurationField(verbose_name='Время круга', null=True, blank=True)
    position = models.PositiveIntegerField(verbose_name='Позиция')
    completed_laps = models.PositiveIntegerField(verbose_name='Пройдено кругов', default=0)

    class Meta:
        ordering = ['position']
        verbose_name = 'Результат гонки'
        verbose_name_plural = 'Результаты гонок'
        unique_together = ['race', 'position']

    def __str__(self):
        return f"{self.user} - {self.race} - Позиция: {self.position}"

    def get_lap_time_display(self):
        if self.lap_time:
            total_seconds = int(self.lap_time.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes:02d}:{seconds:02d}"
        return "-"