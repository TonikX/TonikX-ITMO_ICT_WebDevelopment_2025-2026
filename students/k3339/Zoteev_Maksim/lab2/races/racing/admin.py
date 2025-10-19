from django.contrib import admin
from .models import Team, Car, Participant, Race, RaceParticipant, Comment


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "founded_year", "created_at"]
    list_filter = ["country", "founded_year"]
    search_fields = ["name", "country", "description"]
    ordering = ["name"]


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["model_name", "manufacturer", "year", "horsepower", "created_at"]
    list_filter = ["manufacturer", "year"]
    search_fields = ["model_name", "manufacturer", "engine_type"]
    ordering = ["-year", "model_name"]


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "country",
        "team",
        "car",
        "experience_level",
        "created_at",
    ]
    list_filter = ["experience_level", "country", "team"]
    search_fields = ["full_name", "country", "bio"]
    ordering = ["full_name"]
    raw_id_fields = ["user"]


class RaceParticipantInline(admin.TabularInline):
    model = RaceParticipant
    extra = 1
    fields = [
        "participant",
        "position",
        "finish_time",
        "best_lap_time",
        "points",
        "dnf",
        "dnf_reason",
    ]


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "location",
        "date",
        "status",
        "track_length",
        "total_laps",
        "created_at",
    ]
    list_filter = ["status", "location", "date"]
    search_fields = ["name", "location", "description"]
    ordering = ["-date"]
    date_hierarchy = "date"
    inlines = [RaceParticipantInline]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "location", "date", "status")}),
        ("Track Details", {"fields": ("track_length", "total_laps", "description")}),
    )


@admin.register(RaceParticipant)
class RaceParticipantAdmin(admin.ModelAdmin):
    list_display = ["participant", "race", "position", "finish_time", "points", "dnf"]
    list_filter = ["race", "dnf", "position"]
    search_fields = ["participant__full_name", "race__name"]
    ordering = ["race", "position"]
    raw_id_fields = ["race", "participant"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "race", "comment_type", "rating", "created_at"]
    list_filter = ["comment_type", "rating", "created_at"]
    search_fields = ["author__username", "race__name", "text"]
    ordering = ["-created_at"]
    raw_id_fields = ["race", "author"]
    readonly_fields = ["created_at", "updated_at"]
