from django.contrib import admin

from .models import Stay


@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ('client', 'room', 'check_in', 'check_out', 'status', 'total_cost')
    list_filter = ('status', 'room__room_type')
    search_fields = ('client__last_name', 'room__number')
