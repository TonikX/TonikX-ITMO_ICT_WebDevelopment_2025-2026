from django.contrib import admin

from .models import Reservation, Review, Tour


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency', 'country', 'start_date', 'end_date', 'price')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'passengers_count', 'status')
    list_filter = ('status',)
    actions = ['confirm_reservations']

    def confirm_reservations(self, request, queryset):
        queryset.update(status='подтвержден')
    confirm_reservations.short_description = "Подтвердить выбранные бронирования"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'rating', 'tour_start_date', 'tour_end_date')