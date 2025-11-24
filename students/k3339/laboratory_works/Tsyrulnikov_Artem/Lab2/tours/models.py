import base64

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Tour(models.Model):
    name = models.CharField(max_length=120)
    agency = models.CharField(max_length=120)
    description = models.TextField()
    country = models.CharField(max_length=80)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.TextField()
    image = models.BinaryField(blank=True, null=True)
    image_mime = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self) -> str:
        return f"{self.name} ({self.country})"

    @property
    def image_data_url(self) -> str | None:
        if self.image and self.image_mime:
            encoded = base64.b64encode(self.image).decode("ascii")
            return f"data:{self.image_mime};base64,{encoded}"
        return None


class Reservation(models.Model):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (PENDING, "В ожидании"),
        (CONFIRMED, "Подтверждено"),
        (CANCELLED, "Отменено"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    guests = models.PositiveSmallIntegerField(default=1)
    travel_start = models.DateField()
    travel_end = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PENDING)
    reserved_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "tour", "travel_start", "travel_end")
        ordering = ["-reserved_at"]

    def __str__(self) -> str:
        return f"{self.user} → {self.tour}"


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tour_start = models.DateField()
    tour_end = models.DateField()
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not (1 <= self.rating <= 10):
            raise ValueError("Rating must be between 1 and 10.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.tour} / {self.rating}"
