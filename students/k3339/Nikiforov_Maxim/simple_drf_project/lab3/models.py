from django.db import models


class CarOwner(models.Model):
	surname = models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	birth_date = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.surname} {self.name}"


class Car(models.Model):
	plate_number = models.CharField(max_length=15)
	brand = models.CharField(max_length=20)
	model = models.CharField(max_length=20)
	color = models.CharField(max_length=30, null=True, blank=True)

	def __str__(self):
		return f"{self.brand} {self.model} ({self.plate_number})"


class DriverLicense(models.Model):
	owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='licenses')
	license_number = models.CharField(max_length=10)
	license_type = models.CharField(max_length=10)
	issue_date = models.DateTimeField()

	def __str__(self):
		return f"{self.license_number} ({self.license_type}) - {self.owner}"


class Ownership(models.Model):
	owner = models.ForeignKey(CarOwner, null=True, blank=True, on_delete=models.SET_NULL, related_name='ownerships')
	car = models.ForeignKey(Car, null=True, blank=True, on_delete=models.SET_NULL, related_name='ownerships')
	start_date = models.DateTimeField(null=True, blank=True)
	end_date = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		owner = self.owner or "(no owner)"
		car = self.car or "(no car)"
		return f"Ownership: {owner} -> {car}"
