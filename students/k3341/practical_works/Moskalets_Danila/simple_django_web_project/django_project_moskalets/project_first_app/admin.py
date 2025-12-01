from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CarOwner, DriverLicense, Car, Ownership, CarUser


class OwnershipInline(admin.TabularInline):
    model = Ownership
    extra = 1


class DriverLicenseInline(admin.StackedInline):
    model = DriverLicense
    extra = 1


@admin.register(CarOwner)
class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ('id_owner', 'last_name', 'first_name', 'birth_date')
    list_filter = ('last_name', 'birth_date')
    search_fields = ('last_name', 'first_name')
    inlines = [DriverLicenseInline, OwnershipInline]


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'brand', 'model', 'color')
    list_filter = ('brand', 'model')
    search_fields = ('license_plate', 'brand', 'model')


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('id_license', 'id_owner', 'license_number', 'license_type', 'issue_date')
    list_filter = ('license_type', 'issue_date')
    search_fields = ('license_number', 'id_owner__last_name')


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('id_owner', 'id_car', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('id_owner__last_name', 'id_car__license_plate')


@admin.register(CarUser)
class CarUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('passport_number', 'home_address', 'nationality', 'car_owner_profile')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('passport_number', 'home_address', 'nationality', 'car_owner_profile')
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'nationality')
    list_filter = ('nationality', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'passport_number')