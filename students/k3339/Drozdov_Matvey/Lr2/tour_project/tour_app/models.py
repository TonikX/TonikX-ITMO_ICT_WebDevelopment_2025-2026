from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class TourAgency(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Tour(models.Model):
    title = models.CharField(max_length=255)
    agency = models.ForeignKey(TourAgency, on_delete=models.CASCADE)
    description = models.TextField()
    country = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_terms = models.TextField()

    def __str__(self):
        return self.title

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} — {self.tour.title}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.tour.title} — {self.rating}/10"



