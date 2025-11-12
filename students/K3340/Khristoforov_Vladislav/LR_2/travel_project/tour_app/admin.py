from django.contrib import admin
from .models import Tour, Booking, Review

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'agency', 'country', 'start_date', 'end_date', 'price', 'available_spots_display']
    list_filter = ['country', 'start_date', 'agency']
    search_fields = ['title', 'description']
    
    def available_spots_display(self, obj):
        return f"{obj.get_available_spots()}/{obj.available_spots}"
    available_spots_display.short_description = 'Свободно/Всего'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'booking_date', 'persons', 'status']
    list_filter = ['status', 'booking_date']
    actions = ['confirm_bookings']
    
    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_bookings.short_description = "Подтвердить выбранные бронирования"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'rating', 'review_date']
    list_filter = ['rating', 'review_date']