from django.contrib import admin
from .models import Amenity, Hotel, RoomType, Room, Reservation, Review

@admin.action(description="Заселить (checked_in)")
def check_in(modeladmin, request, queryset):
    queryset.update(status="checked_in")

@admin.action(description="Выселить (checked_out)")
def check_out(modeladmin, request, queryset):
    queryset.update(status="checked_out")

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room", "check_in", "check_out", "status", "created_at")
    list_filter = ("status", "room__hotel")
    search_fields = ("user__username", "room__number", "room__hotel__name")
    actions = [check_in, check_out]

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "address")
    search_fields = ("name", "owner__username", "address")
    filter_horizontal = ("amenities",)

admin.site.register(Amenity)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Review)
