from django.contrib import admin
from .models import CustomUser, Building, Apartment, ServiceCategory, ServiceRequest, MeterReading


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    ordering = ['last_name', 'first_name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'birth_date')}),
        ('Роль и права', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['address', 'total_floors', 'year_built', 'total_apartments', 'created_at']
    list_filter = ['year_built', 'total_floors']
    search_fields = ['address', 'description']
    ordering = ['address']


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['number', 'building', 'floor', 'rooms', 'area', 'balance', 'owner']
    list_filter = ['building', 'floor', 'rooms']
    search_fields = ['number', 'building__address']
    ordering = ['building', 'number']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'priority', 'apartment', 'requester', 'worker', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'assigned_at', 'started_at', 'resolved_at']
    fieldsets = (
        ('Основная информация', {'fields': ('title', 'description', 'status', 'priority', 'category')}),
        ('Связи', {'fields': ('apartment', 'requester', 'worker')}),
        ('Даты', {'fields': ('created_at', 'updated_at', 'assigned_at', 'started_at', 'resolved_at')}),
        ('Комментарии', {'fields': ('worker_comment',)}),
    )


@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ['meter_type', 'value', 'previous_value', 'consumption', 'apartment', 'date_recorded']
    list_filter = ['meter_type', 'date_recorded']
    search_fields = ['apartment__number', 'apartment__building__address']
    ordering = ['-date_recorded', '-created_at']
    readonly_fields = ['consumption', 'created_at']

