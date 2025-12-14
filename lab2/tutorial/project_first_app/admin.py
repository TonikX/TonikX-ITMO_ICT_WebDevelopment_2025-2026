from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Car, Ownership, DriverLicense


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Расширенная админка для пользователей-владельцев автомобилей"""
    # Добавляем новые поля в fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('passport_number', 'home_address', 'nationality', 'birth_date')
        }),
    )
    
    # Добавляем новые поля в add_fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('passport_number', 'home_address', 'nationality', 'birth_date')
        }),
    )
    
    # Поля для отображения в списке
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'nationality', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'nationality', 'birth_date')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'passport_number')
    ordering = ('username',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'color', 'state_number')
    list_filter = ('brand', 'color')
    search_fields = ('brand', 'model', 'state_number')


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('owner', 'car', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('owner__first_name', 'owner__last_name', 'owner__username', 'car__brand', 'car__model')


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('owner', 'license_number', 'license_type', 'issue_date')
    list_filter = ('license_type', 'issue_date')
    search_fields = ('owner__first_name', 'owner__last_name', 'owner__username', 'license_number')
