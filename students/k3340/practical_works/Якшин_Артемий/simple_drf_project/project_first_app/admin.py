from django.contrib import admin
from .models import CarOwner, DriverLicense, Car, Ownership


@admin.register(CarOwner)
class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'birth_date')
    search_fields = ('last_name', 'first_name')


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'license_number', 'license_type', 'owner', 'issue_date')
    search_fields = ('license_number',)
    list_filter = ('license_type',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'license_plate', 'brand', 'model', 'color')
    search_fields = ('license_plate', 'brand', 'model')
    list_filter = ('brand', 'color')


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'car', 'start_date', 'end_date')
    list_filter = ('start_date',)


