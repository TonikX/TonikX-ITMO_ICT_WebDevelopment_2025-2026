from django.contrib import admin
from .models import Country, TourAgency, Tour, Reservation, Review


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(TourAgency)
class TourAgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'agency', 'start_date', 'end_date', 'price']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'status', 'num_people', 'created_at']
    list_editable = ['status']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'tour__name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'rating', 'created_at']
