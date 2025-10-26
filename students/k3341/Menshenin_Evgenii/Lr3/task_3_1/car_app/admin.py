from django.contrib import admin
from .models import CarOwner, DriverLicense, Car, Ownership

# Register your models here.
admin.site.register(CarOwner)
admin.site.register(DriverLicense)
admin.site.register(Car)
admin.site.register(Ownership)