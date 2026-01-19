from django.contrib import admin
from .models import Tour, Reservation, Review


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'travel_agency', 'country', 'start_date', 'end_date', 'created_at')
    list_filter = ('country', 'travel_agency', 'start_date')
    search_fields = ('title', 'description', 'travel_agency', 'country')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'reservation_date', 'status', 'get_tour_country')
    list_filter = ('status', 'reservation_date', 'tour__country')
    search_fields = ('user__username', 'tour__title', 'tour__country')
    date_hierarchy = 'reservation_date'
    readonly_fields = ('reservation_date',)
    actions = ['confirm_reservations', 'cancel_reservations']

    def get_tour_country(self, obj):
        return obj.tour.country
    get_tour_country.short_description = 'Страна тура'

    @admin.action(description='Подтвердить выбранные резервирования')
    def confirm_reservations(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} резервирований подтверждено.')

    @admin.action(description='Отменить выбранные резервирования')
    def cancel_reservations(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} резервирований отменено.')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'rating', 'tour_start_date', 'tour_end_date', 'created_at')
    list_filter = ('rating', 'created_at', 'tour__country')
    search_fields = ('user__username', 'tour__title', 'text')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
