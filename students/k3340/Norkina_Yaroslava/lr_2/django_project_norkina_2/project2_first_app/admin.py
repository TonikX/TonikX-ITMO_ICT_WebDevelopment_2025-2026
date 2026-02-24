# carshering/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Model,
    Car,
    Passport,
    DriverLicense,
    Repair,
    Payment,
    Tariff,
    Trip
)

# ========================
# 1. Расширенный пользователь
# ========================
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Добавляем кастомные поля в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные данные', {
            'fields': ('user_name',)
        }),
    )
    # Добавляем кастомные поля в форму создания
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительные данные', {
            'fields': ('user_name', 'first_name', 'last_name')
        }),
    )
    # Отображаем в списке
    list_display = ('username', 'user_name', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'user_name', 'first_name', 'last_name', 'email')


# ========================
# 2. Остальные модели
# ========================

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'power')
    search_fields = ('brand', 'model_name')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('licence', 'model', 'mileage', 'buying_date', 'city')
    list_filter = ('model__brand', 'city')
    search_fields = ('licence', 'serial_number')


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ('user', 'passport_number', 'serial_number', 'birth_date')
    search_fields = ('passport_number', 'serial_number', 'user__user_name')


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_issue', 'expiration_date')
    list_filter = ('date_of_issue', 'expiration_date')
    search_fields = ('user__user_name',)


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('car', 'datetime', 'description')
    list_filter = ('datetime', 'car__licence')
    search_fields = ('description', 'car__licence')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'value', 'date', 'deadline', 'type')
    list_filter = ('date', 'type')
    search_fields = ('user__user_name', 'description')


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('model', 'price_per_minute', 'start_time', 'end_time')
    list_filter = ('model__brand',)
    search_fields = ('model__brand', 'model__model_name')


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_time', 'end_time')
    list_filter = ('start_time', 'car__licence')
    search_fields = ('user__user_name', 'car__licence', 'comments')