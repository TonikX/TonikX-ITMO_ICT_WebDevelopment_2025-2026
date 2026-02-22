from django.db import models


class BusType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.name} ({self.capacity} seats)"


class Bus(models.Model):
    reg_number = models.CharField(max_length=20, unique=True)
    bus_type = models.ForeignKey(BusType, on_delete=models.CASCADE, related_name="buses")
    def __str__(self):
        return f"{self.reg_number} ({self.bus_type.name})"


class Route(models.Model):
    number = models.CharField(max_length=20, unique=True)
    start_point = models.CharField(max_length=200)
    end_point = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval_minutes = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    def __str__(self):
        return f"Route {self.number}: {self.start_point} — {self.end_point}"


class Driver(models.Model):
    CLASS_CHOICES = [
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passport = models.CharField(max_length=20, unique=True)
    driver_class = models.CharField(max_length=1, choices=CLASS_CHOICES)
    experience_years = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True, related_name="drivers")
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name="drivers")
    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Schedule(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="schedules")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="schedules")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="schedules")
    date = models.DateField()
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    class Meta:
        unique_together = ['driver', 'date']
    def __str__(self):
        return f"{self.driver} — {self.route} ({self.date})"


class Absence(models.Model):
    REASON_CHOICES = [
        ('breakdown', 'Bus breakdown'),
        ('no_driver', 'No driver available'),
        ('other', 'Other'),
    ]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="absences")
    date = models.DateField()
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    note = models.TextField(blank=True)
    class Meta:
        unique_together = ['bus', 'date']
    def __str__(self):
        return f"{self.bus} — {self.date} ({self.get_reason_display()})"
