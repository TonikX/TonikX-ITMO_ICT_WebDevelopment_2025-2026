from django.contrib import admin
from .models import Team, ParticipantProfile, Race, Heat, Registration, Comment

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(ParticipantProfile)
class ParticipantProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "team", "driver_class", "experience_years")
    list_filter = ("driver_class", "team")
    search_fields = ("full_name", "user__username")

class HeatInline(admin.TabularInline):
    model = Heat
    extra = 0

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location")
    list_filter = ("date", "location")
    search_fields = ("title",)
    inlines = [HeatInline]

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("participant", "race", "created_at")
    list_filter = ("race",)
    search_fields = ("participant__full_name", "race__title")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("race", "author", "comment_type", "rating", "heat_date", "created_at")
    list_filter = ("comment_type", "rating", "heat_date")
    search_fields = ("text", "author__username", "race__title")
