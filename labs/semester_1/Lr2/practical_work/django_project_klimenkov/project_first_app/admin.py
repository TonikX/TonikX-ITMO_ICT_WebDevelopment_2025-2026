from django.contrib import admin
from .models import Owner, Car, DrivingLicense, Ownership


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'last_name', 'first_name', 'birth_date', 'passport_number', 'address', 'nationality']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_id', 'license_plate', 'model', 'color']


@admin.register(DrivingLicense)
class DrivingLicenseAdmin(admin.ModelAdmin):
    list_display = ['license_id', 'owner', 'license_number', 'license_type', 'issue_date']


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['ownership_id', 'owner', 'car', 'start_date', 'end_date']
