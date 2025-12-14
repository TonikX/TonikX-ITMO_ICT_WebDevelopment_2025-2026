from django.contrib import admin
from .models import Room, Guest, Stay, Employee, CleaningSchedule


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'room_type', 'floor', 'price_per_night', 'phone', 'is_occupied']
    list_filter = ['room_type', 'floor', 'is_occupied']
    search_fields = ['number', 'phone']
    ordering = ['floor', 'number']


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'passport_number', 'city']
    list_filter = ['city']
    search_fields = ['last_name', 'first_name', 'middle_name', 'passport_number', 'city']
    ordering = ['last_name', 'first_name']


@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ['guest', 'room', 'check_in_date', 'check_out_date']
    list_filter = ['check_in_date', 'check_out_date', 'room']
    search_fields = ['guest__last_name', 'guest__first_name', 'room__number']
    date_hierarchy = 'check_in_date'
    ordering = ['-check_in_date']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['last_name', 'first_name', 'middle_name']
    ordering = ['last_name', 'first_name']


@admin.register(CleaningSchedule)
class CleaningScheduleAdmin(admin.ModelAdmin):
    list_display = ['employee', 'floor', 'day_of_week']
    list_filter = ['day_of_week', 'floor']
    search_fields = ['employee__last_name', 'employee__first_name']
    ordering = ['day_of_week', 'floor']
