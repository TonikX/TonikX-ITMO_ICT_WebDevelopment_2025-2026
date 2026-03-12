
from django.contrib import admin
from .models import Owner, Car, DriverLicense, Ownership

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'birth_date']
    search_fields = ['last_name', 'first_name']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'license_plate', 'color']
    search_fields = ['brand', 'model', 'license_plate']

@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ['owner', 'license_number', 'type', 'issue_date']

@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['owner', 'car', 'start_date', 'end_date']