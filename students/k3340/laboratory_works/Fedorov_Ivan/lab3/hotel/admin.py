from django.contrib import admin
from .models import Room, Client, Employee, CleaningSchedule

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'floor', 'room_type', 'price_per_day', 'is_available']
    list_filter = ['room_type', 'floor', 'is_available']
    search_fields = ['number']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'passport', 'city', 'check_in_date', 'room']
    list_filter = ['city', 'check_in_date']
    search_fields = ['last_name', 'first_name', 'passport']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['last_name', 'first_name']

@admin.register(CleaningSchedule)
class CleaningScheduleAdmin(admin.ModelAdmin):
    list_display = ['employee', 'floor', 'day_of_week']
    list_filter = ['day_of_week', 'floor']