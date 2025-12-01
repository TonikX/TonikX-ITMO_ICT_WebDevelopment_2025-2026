from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'floor', 'room_type', 'capacity', 'daily_rate', 'is_active')
    list_filter = ('room_type', 'floor', 'is_active')
    search_fields = ('number',)
