from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Team(models.Model):
    """Racing team model"""

    name = models.CharField(max_length=200, unique=True, verbose_name="Team Name")
    country = models.CharField(max_length=100, verbose_name="Country")
    founded_year = models.IntegerField(verbose_name="Founded Year")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name


class Car(models.Model):
    """Racing car model"""

    model_name = models.CharField(max_length=200, verbose_name="Model Name")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    year = models.IntegerField(verbose_name="Year")
    engine_type = models.CharField(max_length=100, verbose_name="Engine Type")
    horsepower = models.IntegerField(verbose_name="Horsepower (HP)")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "model_name"]
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return f"{self.manufacturer} {self.model_name} ({self.year})"


class Participant(models.Model):
    """Race participant (driver) model"""

    EXPERIENCE_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("professional", "Professional"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="participant_profile"
    )
    full_name = models.CharField(max_length=200, verbose_name="Full Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    country = models.CharField(max_length=100, verbose_name="Country")
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="participants",
        verbose_name="Team",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drivers",
        verbose_name="Car",
    )
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="beginner",
        verbose_name="Experience Level",
    )
    bio = models.TextField(blank=True, verbose_name="Biography")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def __str__(self):
        return self.full_name


class Race(models.Model):
    """Race event model"""

    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=200, verbose_name="Race Name")
    location = models.CharField(max_length=200, verbose_name="Location")
    track_length = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Track Length (km)"
    )
    total_laps = models.IntegerField(verbose_name="Total Laps")
    date = models.DateTimeField(verbose_name="Race Date")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="upcoming", verbose_name="Status"
    )
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Race"
        verbose_name_plural = "Races"

    def __str__(self):
        return f"{self.name} - {self.location} ({self.date.strftime('%Y-%m-%d')})"

    @property
    def is_upcoming(self):
        return self.status == "upcoming" and self.date > timezone.now()

    @property
    def is_completed(self):
        return self.status == "completed"


class RaceParticipant(models.Model):
    """Race participation and results model"""

    race = models.ForeignKey(
        Race, on_delete=models.CASCADE, related_name="participants", verbose_name="Race"
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="race_entries",
        verbose_name="Participant",
    )
    position = models.IntegerField(null=True, blank=True, verbose_name="Final Position")
    finish_time = models.DurationField(
        null=True, blank=True, verbose_name="Finish Time"
    )
    best_lap_time = models.DurationField(
        null=True, blank=True, verbose_name="Best Lap Time"
    )
    points = models.IntegerField(default=0, verbose_name="Points")
    dnf = models.BooleanField(default=False, verbose_name="Did Not Finish")
    dnf_reason = models.CharField(max_length=200, blank=True, verbose_name="DNF Reason")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["race", "position"]
        unique_together = ["race", "participant"]
        verbose_name = "Race Participant"
        verbose_name_plural = "Race Participants"

    def __str__(self):
        return f"{self.participant.full_name} - {self.race.name}"


class Comment(models.Model):
    """Comment/review model for races"""

    COMMENT_TYPE_CHOICES = [
        ("cooperation", "Cooperation Issue"),
        ("track", "Track Condition"),
        ("other", "Other"),
    ]

    race = models.ForeignKey(
        Race, on_delete=models.CASCADE, related_name="comments", verbose_name="Race"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", verbose_name="Author"
    )
    comment_type = models.CharField(
        max_length=20, choices=COMMENT_TYPE_CHOICES, verbose_name="Comment Type"
    )
    text = models.TextField(verbose_name="Comment Text")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Rating (1-10)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.author.username} - {self.race.name} ({self.rating}/10)"
