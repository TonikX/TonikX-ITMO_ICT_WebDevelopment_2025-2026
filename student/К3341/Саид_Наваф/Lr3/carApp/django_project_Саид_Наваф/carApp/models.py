# app/models.py (append or update)
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Owner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OwnerContact(models.Model):
    owner = models.ForeignKey(Owner, related_name='contacts', on_delete=models.CASCADE)
    type = models.CharField(max_length=30)  # phone/email/address
    value = models.CharField(max_length=250)
    is_primary = models.BooleanField(default=False)

class DriverLicense(models.Model):
    owner = models.OneToOneField(Owner, related_name='driver_license', on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    license_type = models.CharField(max_length=10, null=True, blank=True) 
    issue_date = models.DateField()
    issued_by = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

class VehicleModel(models.Model):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    segment = models.CharField(max_length=50, null=True, blank=True)
    year_from = models.IntegerField(null=True, blank=True)
    year_to = models.IntegerField(null=True, blank=True)

class Car(models.Model):
    vehicle_model = models.ForeignKey(VehicleModel, null=True, blank=True, related_name='cars', on_delete=models.SET_NULL)
    color = models.CharField(max_length=50, null=True, blank=True)
    vin = models.CharField(max_length=50, unique=True)
    registration_number = models.CharField(max_length=20, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

class Ownership(models.Model):
    owner = models.ForeignKey(Owner, related_name='ownerships', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='ownerships', on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'car', 'date_start'], name='unique_owner_car_date_start')
        ]

    def clean(self):
        # Validate no overlapping periods for the same owner+car
        qs = Ownership.objects.filter(owner=self.owner, car=self.car).exclude(pk=self.pk)
        for o in qs:
            # overlap if (start <= o.end or o.end is None) and (o.start <= end or end is None)
            if self.date_end is None and o.date_end is None:
                raise ValidationError("Overlapping ownership period exists.")
            start = self.date_start
            end = self.date_end or timezone.datetime.max.date()
            o_start = o.date_start
            o_end = o.date_end or timezone.datetime.max.date()
            if (start <= o_end) and (o_start <= end):
                raise ValidationError("Overlapping ownership period exists.")
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class InsurancePolicy(models.Model):
    car = models.ForeignKey(Car, related_name='policies', on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=80, unique=True)
    insurer = models.CharField(max_length=150)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    sum_insured = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

class ServiceRecord(models.Model):
    car = models.ForeignKey(Car, related_name='services', on_delete=models.CASCADE)
    date = models.DateField()
    mileage = models.IntegerField(null=True, blank=True)
    description = models.TextField()

class Registration(models.Model):
    car = models.ForeignKey(Car, related_name='registrations', on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=40)
    authority = models.CharField(max_length=200, null=True, blank=True)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)