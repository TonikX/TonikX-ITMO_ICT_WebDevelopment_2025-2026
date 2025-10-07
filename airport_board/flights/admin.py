from django.contrib import admin
from .models import Flight, Reservation, Passenger, Review


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'airline', 'departure_time', 'arrival_time', 
                    'flight_type', 'gate_number', 'total_seats', 'available_seats']
    list_filter = ['flight_type', 'airline', 'departure_time']
    search_fields = ['flight_number', 'airline']
    ordering = ['departure_time']


class PassengerInline(admin.StackedInline):
    model = Passenger
    extra = 0
    can_delete = False


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'flight', 'seat_number', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'flight']
    search_fields = ['user__username', 'flight__flight_number']
    ordering = ['-created_at']
    inlines = [PassengerInline]


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'ticket_number', 'passport_number', 
                    'get_flight', 'get_user']
    list_filter = ['reservation__flight']
    search_fields = ['first_name', 'last_name', 'ticket_number', 'passport_number']
    
    def get_flight(self, obj):
        return obj.reservation.flight.flight_number
    get_flight.short_description = 'Рейс'
    
    def get_user(self, obj):
        return obj.reservation.user.username
    get_user.short_description = 'Пользователь'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'flight', 'flight_date', 'rating', 'created_at']
    list_filter = ['rating', 'flight_date', 'flight']
    search_fields = ['user__username', 'flight__flight_number', 'comment']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
