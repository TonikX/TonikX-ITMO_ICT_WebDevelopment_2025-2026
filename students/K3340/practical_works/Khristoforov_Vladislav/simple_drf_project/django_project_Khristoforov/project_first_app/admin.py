from django.contrib import admin

from .models import Car_Owner, Car, Driving_License, Car_Ownership

admin.site.register(Car_Owner)
admin.site.register(Car)
admin.site.register(Driving_License)
admin.site.register(Car_Ownership)
