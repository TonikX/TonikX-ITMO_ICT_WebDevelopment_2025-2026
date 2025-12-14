from django.db import models

class Airport(models.Model):
    airport_code = models.CharField(max_length=10, primary_key=True)
    country = models.CharField(max_length=255)
    status = models.CharField(max_length=30)
    city = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.airport_code})"

class Company(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Plane(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    flight_duration = models.IntegerField()
    mark = models.CharField(max_length=255)
    last_technical_service = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Plane {self.id} - {self.company.name}"

class Flight(models.Model):
    plane = models.ForeignKey(Plane, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departure_flights")
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrival_flights")
    arrival_time = models.DateTimeField()
    arrival_time_fact = models.DateTimeField()
    departure_time = models.DateTimeField()
    departure_time_fact = models.DateTimeField()

    def __str__(self):
        return f"Flight {self.id} from {self.departure_airport} to {self.destination_airport}"

class Seat(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=3)
    seat_type = models.CharField(max_length=50)
    base_price = models.FloatField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} on Flight {self.flight.id}"

class Passenger(models.Model):
    full_name = models.CharField(max_length=255)
    passport_serial = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=255)
    passport_region = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    sale_channel = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    additional_fee = models.FloatField()

    def __str__(self):
        return f"Ticket {self.id} for {self.passenger.full_name}"

class CrewMember(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    passport_serial = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=255)
    passport_region = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class Crew(models.Model):
    member = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    medical_check_date = models.DateTimeField()
    medical_status = models.CharField(max_length=255)
    medical_reason = models.CharField(max_length=255, null=True, blank=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    def __str__(self):
        return f"Crew {self.member.full_name} on Flight {self.flight.id}"
