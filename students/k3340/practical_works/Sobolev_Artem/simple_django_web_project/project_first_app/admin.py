from django.contrib import admin

from .models import CarOwner, Car, Owner, DriverLicense

admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(Owner)
admin.site.register(DriverLicense)