from django.db import models
from django.contrib.auth.models import User
import uuid


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name="Наименование", max_length=200)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name="Наименование", max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")
    address = models.CharField(verbose_name="Адрес", max_length=200)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Место проведения"
        verbose_name_plural = "Места проведения"


class Conference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name="Наименование", max_length=200)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, verbose_name="Место проведения"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    conditions = models.TextField(verbose_name="Условия участия", blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"


class Registration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE, verbose_name="Конференция"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    registration_date = models.DateField(
        verbose_name="Дата регистрации", auto_now_add=True
    )
    theme = models.CharField(
        verbose_name="Тема доклада", max_length=200, blank=True, null=True
    )
    pub_recommendation = models.BooleanField(
        verbose_name="Рекомендован к публикации", default=False
    )

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.conference.title}"

    class Meta:
        verbose_name = "Регистрация"
        verbose_name_plural = "Регистрации"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE, verbose_name="Конференция"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    content = models.TextField(verbose_name="Комментарий")
    rating = models.IntegerField(verbose_name="Оценка", default=0)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self) -> str:
        return f"Комментарий от {self.user.get_full_name()} к {self.conference.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
