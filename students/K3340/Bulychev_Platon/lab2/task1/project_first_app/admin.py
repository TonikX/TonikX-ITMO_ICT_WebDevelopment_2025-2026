from django.contrib import admin
from .models import CarOwner, Car, Ownership, DriverLicense


@admin.register(CarOwner)
class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'passport_number', 'nationality']
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'passport_number', 'home_address', 'nationality']


admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(DriverLicense)
