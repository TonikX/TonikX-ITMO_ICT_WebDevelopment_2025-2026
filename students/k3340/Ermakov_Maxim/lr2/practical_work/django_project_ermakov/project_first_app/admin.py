from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Car, Ownership, DriverLicense

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'passport_number', 'nationality', 'is_staff')
    search_fields = ('username', 'last_name', 'first_name', 'passport_number')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional info', {
            'fields': ('birth_date', 'passport_number', 'home_address', 'nationality')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('first_name', 'last_name', 'email',
                       'birth_date', 'passport_number', 'home_address', 'nationality')
        }),
    )

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'plate_number', 'color')
    search_fields = ('make', 'model', 'plate_number')
    list_filter = ('color',)

@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('owner', 'car', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')

@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'owner', 'issue_date')
    search_fields = ('number', 'owner__last_name', 'owner__first_name')
    list_filter = ('type', 'issue_date')
