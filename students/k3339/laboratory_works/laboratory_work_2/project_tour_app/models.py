from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Agency(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20)


class Tour(models.Model):
    name = models.CharField(max_length=100)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="tours")
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.TextField()
    country = models.CharField(max_length=100)


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('approved', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


class Review(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    date_posted = models.DateTimeField(auto_now_add=True)
