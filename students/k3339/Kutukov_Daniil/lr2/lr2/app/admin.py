from django.contrib import admin
from .models import City, Location, Conference, Registration, Comment


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "address")
    list_filter = ("city",)
    search_fields = ("title", "address")


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "start_date", "end_date")
    list_filter = ("start_date", "end_date", "location__city")
    search_fields = ("title", "conditions")
    date_hierarchy = "start_date"


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "conference",
        "theme",
        "registration_date",
        "pub_recommendation",
    )
    list_filter = ("pub_recommendation", "conference", "registration_date")
    search_fields = ("user__username", "user__first_name", "user__last_name", "theme")
    list_editable = ("pub_recommendation",)
    date_hierarchy = "registration_date"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "conference", "rating", "created_at")
    list_filter = ("rating", "conference", "created_at")
    search_fields = ("user__username", "content")
    date_hierarchy = "created_at"
