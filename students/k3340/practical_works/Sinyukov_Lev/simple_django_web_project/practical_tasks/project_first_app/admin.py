from django.contrib import admin
from .models import Owner, Car, Ownership, DriverLicense


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'birth_date')
    search_fields = ('first_name', 'last_name')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'plate_number', 'brand', 'model', 'color')
    search_fields = ('plate_number', 'brand', 'model')


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'car', 'date_start', 'date_end')
    list_filter = ('owner', 'car', 'date_start', 'date_end')


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'license_number', 'license_type', 'issue_date')
    list_filter = ('license_type',)
    search_fields = ('license_number', 'owner__last_name', 'owner__first_name')