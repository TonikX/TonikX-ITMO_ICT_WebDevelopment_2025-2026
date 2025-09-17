from django.contrib import admin

from .models import Car, CarOwner, DriverLicense, Ownership

admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(DriverLicense)
admin.site.register(Ownership)
