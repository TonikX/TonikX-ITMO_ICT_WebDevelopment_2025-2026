from django.contrib import admin
from .models import CarOwner, Car, DrivingLicense, Ownership


# Register your models here.
admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(DrivingLicense)
admin.site.register(Ownership)