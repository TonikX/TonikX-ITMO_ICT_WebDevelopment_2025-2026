from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Car, DriverLicense, Ownership


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('passport_number', 'address', 'nationality', 'birth_date')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Доп. информация', {'fields': ('passport_number', 'address', 'nationality', 'birth_date')}),
    )
    list_display = ('id', 'username', 'last_name', 'first_name', 'passport_number', 'nationality')


admin.site.register(User, UserAdmin)


class CarAdmin(admin.ModelAdmin):
    list_display = ('id_car', 'plate_number', 'brand', 'model', 'color')
    search_fields = ('plate_number', 'brand', 'model')


admin.site.register(Car, CarAdmin)


class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('id_license', 'id_owner', 'license_number', 'license_type', 'issue_date')
    list_filter = ('license_type',)
    search_fields = ('license_number',)


admin.site.register(DriverLicense, DriverLicenseAdmin)


class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('id_ownership', 'id_owner', 'id_car', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')


admin.site.register(Ownership, OwnershipAdmin)
