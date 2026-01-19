from django.contrib import admin

from django.contrib import admin
from .models import Tour, Reservation, Review

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency', 'country')
    search_fields = ('name', 'agency', 'country')
    list_filter = ['country']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'reservation_date')
    list_filter = ('tour', 'user', 'reservation_date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')