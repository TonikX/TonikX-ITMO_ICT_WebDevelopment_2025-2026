from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        ordering = ["name"]

    def __str__(self):
        return self.name

class ParticipantProfile(models.Model):
    CLASS_CHOICES = [
        ("amateur", "Любитель"),
        ("pro", "Профессионал"),
        ("junior", "Юниор"),
        ("senior", "Сеньор"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participant_profile")
    full_name = models.CharField("ФИО", max_length=255)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name="participants", verbose_name="Команда")
    car_description = models.TextField("Описание автомобиля", blank=True)
    description = models.TextField("Описание участника", blank=True)
    experience_years = models.PositiveIntegerField("Опыт (лет)", default=0)
    driver_class = models.CharField("Класс участника", max_length=20, choices=CLASS_CHOICES, default="amateur")

    class Meta:
        verbose_name = "Профиль участника"
        verbose_name_plural = "Профили участников"

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"

class Race(models.Model):
    title = models.CharField("Название гонки", max_length=255)
    location = models.CharField("Локация", max_length=255, blank=True)
    date = models.DateField("Дата гонки")

    class Meta:
        verbose_name = "Гонка"
        verbose_name_plural = "Гонки"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title} — {self.date}"

class Heat(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="heats", verbose_name="Гонка")
    number = models.PositiveIntegerField("Номер заезда")
    scheduled_at = models.DateTimeField("Время заезда")
    # Результаты указываются администратором: позиция и/или время круга/заезда
    position = models.PositiveIntegerField("Позиция", null=True, blank=True)
    result_time = models.DurationField("Результат (время)", null=True, blank=True)

    class Meta:
        verbose_name = "Заезд"
        verbose_name_plural = "Заезды"
        unique_together = ("race", "number")
        ordering = ["number"]

    def __str__(self):
        return f"Заезд #{self.number} ({self.race})"

class Registration(models.Model):
    participant = models.ForeignKey(ParticipantProfile, on_delete=models.CASCADE, related_name="registrations", verbose_name="Участник")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="registrations", verbose_name="Гонка")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Регистрация на гонку"
        verbose_name_plural = "Регистрации на гонку"
        unique_together = ("participant", "race")

    def __str__(self):
        return f"{self.participant.full_name} -> {self.race}"

class Comment(models.Model):
    TYPE_CHOICES = [
        ("cooperation", "Вопрос о сотрудничестве"),
        ("race", "Вопрос о гонках"),
        ("other", "Иное"),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="comments", verbose_name="Гонка")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="race_comments", verbose_name="Комментатор")
    heat_date = models.DateField("Дата заезда")
    text = models.TextField("Текст комментария")
    comment_type = models.CharField("Тип комментария", max_length=20, choices=TYPE_CHOICES, default="other")
    rating = models.PositiveIntegerField("Рейтинг", validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Комментарий {self.author} к {self.race}"
