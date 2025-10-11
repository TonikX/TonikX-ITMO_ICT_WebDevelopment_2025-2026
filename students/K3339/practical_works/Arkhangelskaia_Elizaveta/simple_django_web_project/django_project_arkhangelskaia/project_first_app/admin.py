from django.contrib import admin
from .models import CarOwner, DriverLicense, Car, Ownership
from django.contrib.auth.admin import UserAdmin

class CarOwnerAdmin(UserAdmin):
    model = CarOwner
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birth_date', 'passport_number', 'address', 'nationality')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('birth_date', 'passport_number', 'address', 'nationality')}),
    )

admin.site.register(CarOwner, CarOwnerAdmin)
admin.site.register(DriverLicense)
admin.site.register(Car)
admin.site.register(Ownership)