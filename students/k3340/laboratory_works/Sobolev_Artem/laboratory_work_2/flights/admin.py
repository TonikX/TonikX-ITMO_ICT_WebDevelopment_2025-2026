from django.contrib import admin
from .models import Airport, Airline, Flight, Reservation, Review

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country")
    search_fields = ("name", "city", "country")

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

class ReservationInline(admin.TabularInline):
    model = Reservation
    fields = ("passenger", "seat_number", "ticket_number")
    extra = 1

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("number", "airline", "origin_airport", "destination_airport",
                    "departure_time", "arrival_time")
    list_filter = ("airline", "origin_airport", "destination_airport")
    inlines = [ReservationInline]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("flight", "passenger", "seat_number", "ticket_number", "created_at")
    search_fields = ("seat_number", "ticket_number", "passenger__username", "flight__number")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("flight", "author", "rating", "created_at")
    search_fields = ("author__username", "flight__number")
