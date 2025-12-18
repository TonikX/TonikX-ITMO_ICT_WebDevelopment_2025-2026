from django.contrib import admin
from .models import Tour, Reservation, Review


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'agency', 'country', 'start_date', 'end_date', 'price', 'max_participants']
    list_filter = ['country', 'agency', 'start_date']
    search_fields = ['title', 'agency', 'country', 'description']
    ordering = ['start_date']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'participants_count', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'tour__country']
    search_fields = ['user__username', 'tour__title']
    ordering = ['-created_at']
    
    actions = ['confirm_reservations', 'cancel_reservations']
    
    def confirm_reservations(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} резервирований подтверждено.')
    confirm_reservations.short_description = "Подтвердить выбранные резервирования"
    
    def cancel_reservations(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} резервирований отменено.')
    cancel_reservations.short_description = "Отменить выбранные резервирования"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'rating', 'tour_date', 'created_at']
    list_filter = ['rating', 'tour_date', 'created_at', 'tour__country']
    search_fields = ['user__username', 'tour__title', 'comment']
    ordering = ['-created_at']

