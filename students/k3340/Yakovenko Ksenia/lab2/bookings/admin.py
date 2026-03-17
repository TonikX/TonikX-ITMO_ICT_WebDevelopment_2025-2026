from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("tour", "user", "is_confirmed", "created_at")
    list_filter = ("is_confirmed", "created_at")
    search_fields = ("tour__title", "user__username", "user__email")
    actions = ["confirm_bookings"]

    @admin.action(description="Подтвердить выбранные брони")
    def confirm_bookings(self, request, queryset):
        queryset.update(is_confirmed=True)
