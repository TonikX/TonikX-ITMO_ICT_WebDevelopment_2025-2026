from django.contrib import admin
from .models import Hotel, RoomType, Booking, Review

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'created_at')
    list_filter = ('owner',)
    search_fields = ('name', 'address')
    date_hierarchy = 'created_at'

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'price_per_night', 'capacity')
    list_filter = ('hotel',)
    search_fields = ('name', 'hotel__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_type', 'check_in', 'check_out', 'status', 'total_price')
    list_filter = ('status', 'check_in', 'room_type__hotel')
    search_fields = ('user__username', 'user__first_name', 'room_type__name')
    date_hierarchy = 'check_in'
    readonly_fields = ('total_price', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'rating', 'created_at')
    list_filter = ('rating', 'booking__room_type__hotel')
    search_fields = ('user__username', 'comment')
    date_hierarchy = 'created_at'