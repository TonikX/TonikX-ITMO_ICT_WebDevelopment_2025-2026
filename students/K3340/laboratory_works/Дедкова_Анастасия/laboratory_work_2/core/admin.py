from django.contrib import admin
from .models import Airline, Gate, Flight, Booking, Review


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)


@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
    list_display = ("code", "terminal")
    search_fields = ("code", "terminal")
    ordering = ("terminal", "code")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "airline",
        "departure_airport",
        "arrival_airport",
        "departure_dt",
        "arrival_dt",
        "direction",
        "gate",
        "seats_available",
        "seats_total",
    )
    list_filter = ("direction", "airline")
    search_fields = ("number", "departure_airport", "arrival_airport", "airline__name", "airline__code")
    ordering = ("departure_dt",)
    autocomplete_fields = ("airline", "gate")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "flight", "ticket_number", "created_at")
    list_filter = ("flight__airline", "flight__direction")
    search_fields = ("ticket_number", "user__username", "user__first_name", "user__last_name", "flight__number")
    autocomplete_fields = ("user", "flight")
    ordering = ("-created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("flight", "author", "rating", "flight_date", "created_at")
    list_filter = ("rating", "flight__airline")
    search_fields = ("flight__number", "author__username", "body")
    autocomplete_fields = ("flight", "author")
    ordering = ("-created_at",)
