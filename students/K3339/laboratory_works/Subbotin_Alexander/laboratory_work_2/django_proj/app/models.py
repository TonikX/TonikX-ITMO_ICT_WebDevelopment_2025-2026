from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Tour(models.Model):
    title = models.CharField(max_length=200)
    agency = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    payment_terms = models.TextField(blank=True, null=True, help_text="Условия оплаты")


    def __str__(self):
        return f"{self.title} — {self.city} ({self.start_date} — {self.end_date})"

class Reservation(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    guests = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    confirmed = models.BooleanField(default=False)


    def __str__(self):
        return f"Reservation #{self.id} for {self.tour} by {self.user}"


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField() # 1-10
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review #{self.id} ({self.rating}) on {self.tour}"