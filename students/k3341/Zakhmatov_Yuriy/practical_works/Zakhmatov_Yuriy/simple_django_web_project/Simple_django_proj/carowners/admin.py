from django.contrib import admin
from .models import CarOwner, Car, Ownership, DriverLicense

# Register your models here.

admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(DriverLicense)


