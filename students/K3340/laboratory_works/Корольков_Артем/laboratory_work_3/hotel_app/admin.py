from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_admin', 'is_hotel_staff')
    list_filter = ('is_staff', 'is_admin', 'is_hotel_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные права', {
            'fields': ('is_hotel_staff', 'is_admin')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительные поля', {
            'fields': ('email', 'is_hotel_staff', 'is_admin')
        }),
    )

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'price_per_night')
    list_filter = ('capacity',)
    search_fields = ('name',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'floor', 'room_type', 'is_available')
    list_filter = ('floor', 'room_type', 'is_available')
    search_fields = ('room_number',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'city', 'passport_number')
    list_filter = ('city',)
    search_fields = ('last_name', 'first_name', 'passport_number')

class StaffAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('last_name', 'first_name')

class CleaningScheduleAdmin(admin.ModelAdmin):
    list_display = ('staff', 'floor', 'day_of_week')
    list_filter = ('floor', 'day_of_week')
    search_fields = ('staff__last_name',)

class StayAdmin(admin.ModelAdmin):
    list_display = ('client', 'room', 'check_in_date', 'check_out_date', 'total_cost')
    list_filter = ('check_in_date', 'check_out_date')
    search_fields = ('client__last_name', 'room__room_number')

# Регистрация моделей в админ-панели
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(CleaningSchedule, CleaningScheduleAdmin)
admin.site.register(Stay, StayAdmin)