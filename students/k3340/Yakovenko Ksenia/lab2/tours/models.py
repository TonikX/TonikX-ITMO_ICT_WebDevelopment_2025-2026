from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Agency(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self): return self.name

class Country(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self): return self.name

class Tour(models.Model):
    title = models.CharField(max_length=200)
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT, related_name="tours")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="tours")
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    def __str__(self): return self.title

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    tour_start_date = models.DateField()
    tour_end_date = models.DateField()
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    def __str__(self): return f"{self.tour} - {self.rating}/10"
