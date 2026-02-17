from django.contrib import admin
from .models import Tour, Reservation, Review


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'agency', 'country', 'start_date', 'end_date', 'price']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'rating', 'created_at']
