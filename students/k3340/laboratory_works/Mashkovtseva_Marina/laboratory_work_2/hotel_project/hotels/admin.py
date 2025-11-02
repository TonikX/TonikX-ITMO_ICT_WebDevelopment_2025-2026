from django.contrib import admin
from .models import Hotel, Room, Reservation, Review

@admin.action(description="Заселить (отметить как 'Заселён')")
def make_checked_in(modeladmin, request, queryset):
    queryset.update(status=Reservation.STATUS_CHECKED_IN)

@admin.action(description="Выселить (отметить как 'Выселен')")
def make_checked_out(modeladmin, request, queryset):
    queryset.update(status=Reservation.STATUS_CHECKED_OUT)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'check_in', 'check_out', 'room__hotel')
    search_fields = ('user__username', 'room__hotel__name')
    actions = [make_checked_in, make_checked_out]

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Review)
