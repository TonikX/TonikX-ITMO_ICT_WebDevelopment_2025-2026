from django.contrib import admin
from .models import (
    RoomType, Floor, Room, Guest, Stay, Employee, CleaningSchedule
)


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "capacity", "price_per_day")
    search_fields = ("name",)
    list_filter = ("capacity",)


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "number")
    search_fields = ("number",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "phone", "type", "floor")
    search_fields = ("number", "phone")
    list_filter = ("type", "floor")


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("id", "passport_number", "last_name", "first_name", "city")
    search_fields = ("passport_number", "last_name", "first_name", "city")


@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ("id", "guest", "room", "check_in", "check_out")
    search_fields = ("guest__last_name", "room__number")
    list_filter = ("check_in", "check_out", "room__floor")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "middle_name", "employed")
    search_fields = ("last_name", "first_name")
    list_filter = ("employed",)


@admin.register(CleaningSchedule)
class CleaningScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "weekday", "employee", "floor")
    search_fields = ("weekday", "employee__last_name")
    list_filter = ("weekday", "employee", "floor")
