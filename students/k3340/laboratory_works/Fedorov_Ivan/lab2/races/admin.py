from django.contrib import admin
from .models import Race, RaceRegistration, RaceResult

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'created_at')
    list_filter = ('date',)
    search_fields = ('name', 'description')

@admin.register(RaceRegistration)
class RaceRegistrationAdmin(admin.ModelAdmin):
    list_display = ('race', 'user', 'registration_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'race', 'registration_date')
    search_fields = ('user__username', 'race__name')

@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('race', 'user', 'position', 'lap_time', 'completed_laps')
    list_filter = ('race', 'position')
    search_fields = ('user__username', 'race__name')