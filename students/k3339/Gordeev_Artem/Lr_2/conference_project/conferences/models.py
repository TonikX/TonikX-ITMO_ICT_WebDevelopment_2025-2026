from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Location(models.Model):
    """Модель места проведения конференции."""
    name = models.CharField("Название места", max_length=255)
    address = models.CharField("Адрес", max_length=300)
    description = models.TextField("Описание места", blank=True)

    class Meta:
        verbose_name = "Место проведения"
        verbose_name_plural = "Места проведения"

    def __str__(self):
        return self.name


class Topic(models.Model):
    """Модель тематики конференции."""
    name = models.CharField("Название тематики", max_length=150, unique=True)

    class Meta:
        verbose_name = "Тематика"
        verbose_name_plural = "Тематики"

    def __str__(self):
        return self.name


class Conference(models.Model):
    """Модель научной конференции."""
    title = models.CharField("Название", max_length=255)
    topics = models.ManyToManyField(Topic, verbose_name="Тематики", related_name="conferences")
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Место проведения"
    )
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    description = models.TextField("Описание конференции")
    conditions = models.TextField("Условия участия")

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"
        ordering = ['-start_date']  # сначала новые

    def __str__(self):
        return self.title


class Participation(models.Model):
    """Модель регистрации пользователя на выступление в конференции."""
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participations")
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="participations")
    presentation_title = models.CharField("Тема доклада", max_length=255)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    recommended_for_publication = models.BooleanField(
        "Рекомендован к публикации",
        default=False,
        help_text="Отмечается администратором"
    )

    class Meta:
        verbose_name = "Регистрация на выступление"
        verbose_name_plural = "Регистрации на выступления"
        # один пользователь может зарегистрироваться на конференцию только один раз
        unique_together = ('participant', 'conference')

    def __str__(self):
        return f"{self.participant.username} на '{self.conference.title}'"


class Review(models.Model):
    """Модель отзыва о конференции."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField("Текст комментария")
    rating = models.PositiveSmallIntegerField(
        "Рейтинг",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']  # сначала новые
        unique_together = ('author', 'conference')  # Один пользователь - один отзыв на конференцию

    def __str__(self):
        return f"Отзыв от {self.author.username} на '{self.conference.title}'"
