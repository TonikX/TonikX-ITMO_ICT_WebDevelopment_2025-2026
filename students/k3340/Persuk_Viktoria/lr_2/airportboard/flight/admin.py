from django.contrib import admin
from .models import Flight, Reservation, Comment, AirportAdminProfile


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'departure', 'arrival', 'gate', 'seats_count')
    search_fields = ('flight_number', 'airline', 'gate')
    list_filter = ('flight_type', 'departure')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'flight', 'seat_number', 'ticket_number', 'status', 'created_at')
    search_fields = ('user__username', 'ticket_number', 'seat_number', 'flight__flight_number')
    list_filter = ('status', 'flight')
    autocomplete_fields = ('user', 'flight')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('flight', 'author', 'rating', 'flight_date', 'created_at')
    search_fields = ('author__username', 'flight__flight_number', 'text')
    list_filter = ('rating', 'flight_date')


@admin.register(AirportAdminProfile)
class AirportAdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_airport_admin')
    search_fields = ('user__username', 'user__email')
    list_filter = ('is_airport_admin',)
