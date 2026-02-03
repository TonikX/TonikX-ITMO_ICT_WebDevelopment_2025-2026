"""
Административная панель Django
"""
from django.contrib import admin
from .models import Room, Guest, Staff, CleaningSchedule


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'room_type', 'floor', 'phone', 'price_per_day']
    list_filter = ['room_type', 'floor']
    search_fields = ['number', 'phone']
    ordering = ['number']


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'passport_number', 'city', 'room', 'check_in_date', 'check_out_date', 'is_current']
    list_filter = ['city', 'check_in_date', 'check_out_date']
    search_fields = ['passport_number', 'last_name', 'first_name', 'middle_name']
    date_hierarchy = 'check_in_date'
    ordering = ['-check_in_date']
    
    def is_current(self, obj):
        return obj.is_current
    is_current.boolean = True
    is_current.short_description = 'Проживает'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'is_active', 'hire_date', 'fire_date']
    list_filter = ['is_active', 'hire_date']
    search_fields = ['last_name', 'first_name', 'middle_name']
    date_hierarchy = 'hire_date'
    ordering = ['last_name', 'first_name']


@admin.register(CleaningSchedule)
class CleaningScheduleAdmin(admin.ModelAdmin):
    list_display = ['staff', 'floor', 'weekday']
    list_filter = ['weekday', 'floor']
    search_fields = ['staff__last_name', 'staff__first_name']
    ordering = ['weekday', 'floor']
