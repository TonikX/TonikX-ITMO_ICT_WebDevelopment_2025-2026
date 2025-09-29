from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Airline, Flight, Reservation, Review, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'airline', 'origin', 'destination', 
                   'departure_time', 'arrival_time', 'flight_type', 'gate_number', 'available_seats']
    list_filter = ['airline', 'flight_type', 'departure_time']
    search_fields = ['flight_number', 'origin', 'destination']
    date_hierarchy = 'departure_time'
    ordering = ['departure_time']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'flight', 'seat_number', 'ticket_number', 'created_at']
    list_filter = ['flight__airline', 'created_at']
    search_fields = ['user__username', 'flight__flight_number', 'ticket_number']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'flight' in form.base_fields:
            form.base_fields['flight'].queryset = Flight.objects.select_related('airline')
        return form


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'flight', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'flight__airline']
    search_fields = ['user__username', 'flight__flight_number', 'text']
    readonly_fields = ['created_at']


# Переопределяем стандартную регистрацию User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Настройка заголовков админ-панели
admin.site.site_header = 'Табло авиаперелетов - Администрирование'
admin.site.site_title = 'Табло авиаперелетов'
admin.site.index_title = 'Управление данными'