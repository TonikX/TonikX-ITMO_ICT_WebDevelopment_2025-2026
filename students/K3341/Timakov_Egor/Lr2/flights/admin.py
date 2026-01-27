from django.contrib import admin
from .models import Flight, Reservation, Ticket, Review


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'departure_time', 'arrival_time', 'flight_type', 'gate_number', 'total_seats')
    list_filter = ('flight_type', 'airline', 'departure_time')
    search_fields = ('flight_number', 'airline', 'gate_number')
    date_hierarchy = 'departure_time'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'seat_number', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'flight')
    search_fields = ('user__username', 'flight__flight_number', 'seat_number')
    raw_id_fields = ('user', 'flight')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'passenger_name', 'passenger_passport', 'reservation', 'created_at')
    search_fields = ('ticket_number', 'passenger_name', 'passenger_passport')
    raw_id_fields = ('reservation',)
    
    def save_model(self, request, obj, form, change):
        """Автоматически создаем резервирование, если его нет"""
        if not change:  # Если создаем новый билет
            if not hasattr(obj.reservation, 'ticket'):
                obj.reservation.status = 'confirmed'
                obj.reservation.save()
        super().save_model(request, obj, form, change)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'flight_date', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'flight')
    search_fields = ('user__username', 'flight__flight_number', 'text')
    raw_id_fields = ('user', 'flight')



