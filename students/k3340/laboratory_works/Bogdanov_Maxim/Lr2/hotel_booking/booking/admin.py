from django.contrib import admin
from django.contrib import messages
from .models import Hotel, Amenity, RoomType, Room, Booking, Review
from .services import can_check_in, can_check_out


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'address']
    date_hierarchy = 'created_at'


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'name', 'capacity', 'price_per_night']
    list_filter = ['hotel', 'capacity']
    search_fields = ['name', 'hotel__name']
    filter_horizontal = ['amenities']
    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'get_hotel', 'is_active']
    list_filter = ['is_active', 'room_type__hotel']
    search_fields = ['room_number', 'room_type__name', 'room_type__hotel__name']

    def get_hotel(self, obj):
        return obj.room_type.hotel.name

    get_hotel.short_description = 'Отель'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'check_in', 'check_out', 'status', 'total_price']
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['user__username', 'room__room_number', 'room__room_type__hotel__name']
    date_hierarchy = 'check_in'
    actions = ['check_in_booking', 'check_out_booking']

    def check_in_booking(self, request, queryset):
        """Заселить гостей"""
        success_count = 0
        for booking in queryset:
            if can_check_in(booking):
                booking.status = 'checked_in'
                booking.save()
                success_count += 1
            else:
                self.message_user(
                    request,
                    f'Бронирование {booking.id} нельзя перевести в статус "Заселён" '
                    f'(текущий статус: {booking.get_status_display()}, дата заезда: {booking.check_in})',
                    level=messages.WARNING
                )

        if success_count:
            self.message_user(
                request,
                f'Успешно заселено гостей: {success_count}',
                level=messages.SUCCESS
            )

    check_in_booking.short_description = 'Заселить выбранных гостей'

    def check_out_booking(self, request, queryset):
        """Выселить гостей"""
        success_count = 0
        for booking in queryset:
            if can_check_out(booking):
                booking.status = 'checked_out'
                booking.save()
                success_count += 1
            else:
                self.message_user(
                    request,
                    f'Бронирование {booking.id} нельзя перевести в статус "Выселен" '
                    f'(текущий статус: {booking.get_status_display()})',
                    level=messages.WARNING
                )

        if success_count:
            self.message_user(
                request,
                f'Успешно выселено гостей: {success_count}',
                level=messages.SUCCESS
            )

    check_out_booking.short_description = 'Выселить выбранных гостей'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'rating', 'stay_start', 'stay_end', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'room__room_number', 'comment']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']