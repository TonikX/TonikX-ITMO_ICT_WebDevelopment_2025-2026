from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"


class Airline(models.Model):
    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Flight(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Запланирован'),
        ('in_flight', 'В полёте'),
        ('arrived', 'Прибыл'),
        ('delayed', 'Задержан'),
        ('cancelled', 'Отменён')
    ]
    TYPE_CHOICES = [("DEPARTURE", "Вылет"), ("ARRIVAL", "Прилёт")]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    number = models.CharField(max_length=20)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    gate = models.CharField(max_length=10, blank=True)
    type = models.CharField(max_length=9, choices=TYPE_CHOICES)
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    origin_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="arrival_after_departure",
                check=models.Q(arrival_time__gt=models.F("departure_time")),
            )
        ]

    def __str__(self):
        return f"{self.airline}: {self.number}"


class Reservation(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=4)
    ticket_number = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["flight", "seat_number"], name="uniq_seat_per_flight"),
            models.UniqueConstraint(fields=["flight", "passenger"], name="uniq_passenger_per_flight"),
        ]

    def __str__(self):
        return f"{self.passenger} -> {self.flight.number}, seat {self.seat_number}"


class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight_date = models.DateField(editable=False, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["flight", "author"],
                name="uniq_review_per_user_flight",
            ),
        ]

    def __str__(self):
        return f"Review {self.rating}/10 by {self.author} for {self.flight.number}"

