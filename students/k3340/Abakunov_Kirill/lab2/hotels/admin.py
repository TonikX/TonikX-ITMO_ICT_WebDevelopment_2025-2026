from django.contrib import admin
from .models import Hotel, RoomType, Reservation, Review


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'address']
    search_fields = ['name', 'owner', 'address']


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel', 'price', 'capacity', 'available_count']
    list_filter = ['hotel']
    search_fields = ['name', 'hotel__name']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'room_type', 'check_in_date', 'check_out_date', 'status', 'created_at']
    list_filter = ['status', 'check_in_date', 'check_out_date']
    search_fields = ['user__username', 'room_type__name']
    actions = ['check_in_guests', 'check_out_guests']
    
    def check_in_guests(self, request, queryset):
        """Действие для заселения гостей"""
        updated = queryset.filter(status='confirmed').update(status='checked_in')
        self.message_user(request, f'Заселено гостей: {updated}')
    check_in_guests.short_description = 'Заселить выбранных гостей'
    
    def check_out_guests(self, request, queryset):
        """Действие для выселения гостей"""
        updated = queryset.filter(status='checked_in').update(status='checked_out')
        self.message_user(request, f'Выселено гостей: {updated}')
    check_out_guests.short_description = 'Выселить выбранных гостей'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'room_type', 'rating', 'stay_period_start', 'stay_period_end', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'room_type__name', 'comment']
    readonly_fields = ['created_at']
