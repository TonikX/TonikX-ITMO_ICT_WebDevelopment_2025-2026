from django.contrib import admin
from .models import Venue, Topic, Conference, Registration, Review

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name", "address")

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "venue", "start_date", "end_date")
    list_filter = ("venue", "start_date")
    search_fields = ("title", "description")
    filter_horizontal = ("topics",)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "conference", "talk_title", "created_at", "recommended_to_publish")
    list_filter = ("conference", "recommended_to_publish")
    search_fields = ("talk_title", "talk_abstract", "user__username")
    list_editable = ("recommended_to_publish",) # можно отмечать прямо из списка

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("conference", "user", "rating", "created_at")
    list_filter = ("conference", "rating")
    search_fields = ("text", "user__username")