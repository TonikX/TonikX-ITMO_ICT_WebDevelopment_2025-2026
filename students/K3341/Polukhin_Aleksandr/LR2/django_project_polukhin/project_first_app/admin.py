from django.contrib import admin
from .models import Owner, Car, DriverLicense, Ownership

admin.site.register(Owner)
admin.site.register(Car)
admin.site.register(DriverLicense)
admin.site.register(Ownership)