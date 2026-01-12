from django.db import models
from django.contrib.auth.models import User

# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ROLE_CHOICES = [
        ("admin", "Администратор"),
        ("user", "Пользователь"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    def isAdmin(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    model = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Модель: {self.model}"


class Participant(models.Model):
    CLASS_CHOICES = [
        ("Pro", "Профессионал"),
        ("Amateur", "Любитель"),
        ("A", "Класс A"),
        ("B", "Класс B"),
        ("C", "Класс C"),
    ]

    description = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    participant_class = models.CharField(max_length=20, choices=CLASS_CHOICES, default="Amateur")
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name="participants", null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="participant")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        team_name = self.team.name if self.team else "без команды"
        return f"{self.profile.user.username} ({self.get_participant_class_display()}) — команда: {team_name}"


class Race(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="created_races", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Гонка: {self.name} — {self.date}"


class Registration(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="registrations")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="registrations")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="registrations")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("participant", "race", "car")

    def __str__(self):
        return f"{self.participant} — автомобиль: {self.car.model} — гонка: {self.race.name}"


class RaceSession(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="sessions")
    name = models.CharField(max_length=100, default="Заезд")
    order = models.PositiveIntegerField(default=1)
    start_time = models.DateTimeField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.race.name} — {self.name} №{self.order}"


class RaceResult(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name="results")
    session = models.ForeignKey(RaceSession, on_delete=models.CASCADE, related_name="results")
    total_time = models.DurationField()

    class Meta:
        unique_together = ("registration", "session")
        ordering = ["total_time"]

    def __str__(self):
        return f"{self.registration} — результат заезда №{self.session.order}: {self.total_time}"


class Comment(models.Model):
    COMMENT_TYPE = [
        ("cooperation", "Вопрос о сотрудничестве"),
        ("race_question", "Вопрос о гонках"),
        ("other", "Другое"),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="comments")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPE, default="other")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Комментарий от {self.profile.user.username} к гонке '{self.race.name}': {self.text[:30]}"
