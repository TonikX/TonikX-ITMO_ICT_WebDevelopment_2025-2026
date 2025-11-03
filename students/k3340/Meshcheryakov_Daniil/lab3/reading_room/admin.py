from django.contrib import admin
from .models import ReadingRoom, Reader, Reservation, Librarian, Schedule


@admin.register(ReadingRoom)
class ReadingRoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'floor', 'room_type', 'capacity', 'hourly_rate']
    list_filter = ['floor', 'room_type']
    search_fields = ['number', 'description']


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['library_card', 'last_name', 'first_name', 'phone', 'email']
    search_fields = ['library_card', 'last_name', 'first_name', 'phone']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reader', 'reading_room', 'reserved_from', 'reserved_to', 'is_active']
    list_filter = ['is_active', 'reserved_from']
    search_fields = ['reader__last_name', 'reader__first_name', 'reading_room__number']


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'is_active']
    list_filter = ['is_active']
    search_fields = ['last_name', 'first_name']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['librarian', 'weekday', 'floor']
    list_filter = ['weekday', 'floor']
    search_fields = ['librarian__last_name', 'librarian__first_name']

