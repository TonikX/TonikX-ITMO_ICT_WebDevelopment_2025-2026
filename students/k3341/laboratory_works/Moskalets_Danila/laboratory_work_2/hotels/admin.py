from django.contrib import admin
from django.utils import timezone

from .models import Hotel, RoomType, Reservation, Review, GuestStay


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'address']
    search_fields = ['name', 'owner', 'address']
    list_filter = ['owner']


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel', 'price', 'capacity']
    list_filter = ['hotel', 'capacity']
    search_fields = ['name', 'hotel__name']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'room_type', 'check_in', 'check_out', 'status', 'created_at']
    list_filter = ['status', 'check_in', 'check_out', 'room_type__hotel']
    search_fields = ['user__username', 'room_type__name', 'room_type__hotel__name']
    date_hierarchy = 'created_at'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reservation__user__username', 'text']


@admin.register(GuestStay)
class GuestStayAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'actual_check_in', 'actual_check_out']
    list_filter = ['actual_check_in', 'actual_check_out']
    search_fields = ['reservation__user__username', 'reservation__room_type__hotel__name']

    def check_in_guest(self, request, queryset):
        """Действие для заселения гостя"""
        for stay in queryset:
            if not stay.actual_check_in:
                stay.actual_check_in = timezone.now()
                stay.reservation.status = 'checked_in'
                stay.reservation.save()
                stay.save()

    def check_out_guest(self, request, queryset):
        """Действие для выселения гостя"""
        for stay in queryset:
            if stay.actual_check_in and not stay.actual_check_out:
                stay.actual_check_out = timezone.now()
                stay.reservation.status = 'checked_out'
                stay.reservation.save()
                stay.save()

    check_in_guest.short_description = "Заселить выбранных гостей"
    check_out_guest.short_description = "Выселить выбранных гостей"

    actions = [check_in_guest, check_out_guest]