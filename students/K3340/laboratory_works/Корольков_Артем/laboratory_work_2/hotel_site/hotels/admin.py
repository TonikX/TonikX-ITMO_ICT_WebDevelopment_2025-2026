from django.contrib import admin
from .models import Hotel, RoomType, Reservation, Review

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'room_type', 'check_in', 'check_out', 'status', 'created_at']
    list_filter = ['status', 'check_in', 'check_out', 'room_type__hotel']
    search_fields = ['user__username', 'room_type__hotel__name']
    date_hierarchy = 'created_at'
    actions = ['mark_checked_in', 'mark_checked_out', 'mark_canceled']

    def mark_checked_in(self, request, queryset):
        updated = queryset.update(status='checked_in')
        self.message_user(request, f'{updated} бронирований отмечено как "Заселен"')
    mark_checked_in.short_description = "Отметить как заселенные"

    def mark_checked_out(self, request, queryset):
        updated = queryset.update(status='checked_out')
        self.message_user(request, f'{updated} бронирований отмечено как "Выселен"')
    mark_checked_out.short_description = "Отметить как выселенные"

    def mark_canceled(self, request, queryset):
        updated = queryset.update(status='canceled')
        self.message_user(request, f'{updated} бронирований отменено')
    mark_canceled.short_description = "Отменить бронирования"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'room_type', 'rating', 'stay_period', 'created_at']
    list_filter = ['rating', 'created_at', 'room_type__hotel']
    search_fields = ['user__username', 'room_type__hotel__name', 'text']
    readonly_fields = ['created_at']

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'address']
    search_fields = ['name', 'owner', 'address']
    list_filter = ['owner']

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel', 'cost', 'capacity']
    list_filter = ['hotel', 'capacity']
    search_fields = ['name', 'hotel__name']