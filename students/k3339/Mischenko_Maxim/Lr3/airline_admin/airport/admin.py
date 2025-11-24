from django.contrib import admin
from .models import (
    Company, PlaneType, Aircraft,
    Airport, Flight, Stopover,
    CrewMember, Crew, CrewAssignment,
    CrewMemberFlightPermission
)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_airline")

@admin.register(PlaneType)
class PlaneTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "plane_type", "seats", "owner_company")

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("iata_code", "city", "name")

@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "employer", "experience_years")

@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(CrewAssignment)
class CrewAssignmentAdmin(admin.ModelAdmin):
    list_display = ("crew", "member", "role", "is_active")

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("flight_number", "departure_airport", "arrival_airport", "departure_datetime", "arrival_datetime", "aircraft")

@admin.register(Stopover)
class StopoverAdmin(admin.ModelAdmin):
    list_display = ("flight", "order", "airport", "arrival_datetime", "departure_datetime")

@admin.register(CrewMemberFlightPermission)
class CrewMemberFlightPermissionAdmin(admin.ModelAdmin):
    list_display = ("flight", "member", "allowed", "issued_by", "issued_at")
