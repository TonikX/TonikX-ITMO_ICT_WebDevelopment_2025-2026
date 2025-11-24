from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    is_airline = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PlaneType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Aircraft(models.Model):
    registration_number = models.CharField(max_length=50, unique=True)
    plane_type = models.ForeignKey(PlaneType, on_delete=models.PROTECT, related_name="aircrafts")
    seats = models.PositiveIntegerField()
    cruise_speed_kmh = models.PositiveIntegerField()
    owner_company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="aircrafts")

    def __str__(self):
        return f"{self.registration_number} ({self.plane_type.name})"

class Airport(models.Model):
    iata_code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    class Meta:
        unique_together = ("iata_code", "city")

    def __str__(self):
        return f"{self.iata_code} — {self.city} / {self.name}"

class CrewMember(models.Model):
    ROLE_CHOICES = [
        ("CAPTAIN", "Командир корабля"),
        ("FIRST_OFFICER", "Второй пилот"),
        ("NAVIGATOR", "Штурман"),
        ("STEWARD", "Стюард / Стюардесса"),
        ("OTHER", "Другое"),
    ]
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=120, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=255, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    passport_data = models.CharField(max_length=255)
    employer = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")

    def full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join([p for p in parts if p])

    def __str__(self):
        return f"{self.full_name()}"

class Crew(models.Model):
    name = models.CharField(max_length=200, blank=True)
    members = models.ManyToManyField(CrewMember, through="CrewAssignment", related_name="crews")

    def __str__(self):
        return self.name or f"Crew #{self.pk}"

class CrewAssignment(models.Model):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    member = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    role = models.CharField(max_length=32, choices=CrewMember.ROLE_CHOICES)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("crew", "member")

    def __str__(self):
        return f"{self.member} as {self.get_role_display()} in {self.crew}"

class Flight(models.Model):
    flight_number = models.CharField(max_length=50, unique=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name="flights")
    distance_km = models.FloatField()
    departure_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="departing_flights")
    arrival_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="arriving_flights")
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    crew = models.ForeignKey(Crew, on_delete=models.SET_NULL, null=True, blank=True, related_name="flights")
    sold_tickets = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.flight_number}: {self.departure_airport.iata_code} → {self.arrival_airport.iata_code}"

class Stopover(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="stopovers")
    order = models.PositiveIntegerField()
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    arrival_datetime = models.DateTimeField()
    departure_datetime = models.DateTimeField()

    class Meta:
        ordering = ["order"]
        unique_together = ("flight", "order")

    def __str__(self):
        return f"{self.flight.flight_number} stop {self.order} @ {self.airport.iata_code}"

class CrewMemberFlightPermission(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="crew_permissions")
    member = models.ForeignKey(CrewMember, on_delete=models.CASCADE, related_name="flight_permissions")
    allowed = models.BooleanField(default=False)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ("flight", "member")

    def __str__(self):
        return f"{self.member} permission for {self.flight}: {'OK' if self.allowed else 'NO'}"
