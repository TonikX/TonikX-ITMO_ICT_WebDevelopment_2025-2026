from django.contrib import admin
from .models import Topic, Place, Conference, Registration, Review

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name", "address", "description")

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "place", "start_date", "end_date")
    list_filter = ("start_date", "end_date", "topics", "place")
    search_fields = ("title", "description", "participation_terms", "place__name")
    filter_horizontal = ("topics",)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "conference", "presentation_title", "result", "created")
    list_filter = ("result", "conference")
    search_fields = ("user__username", "presentation_title", "conference__title")
    list_editable = ("result",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("conference", "user", "rating", "date_posted")
    list_filter = ("rating", "conference")
    search_fields = ("user__username", "conference__title", "text")

