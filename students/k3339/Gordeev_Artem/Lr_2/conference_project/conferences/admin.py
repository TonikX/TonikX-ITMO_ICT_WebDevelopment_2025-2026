from django.contrib import admin

from .models import Location, Topic, Conference, Participation, Review


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'end_date')
    list_filter = ('start_date', 'location', 'topics')
    search_fields = ('title', 'description')
    filter_horizontal = ('topics',)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'conference', 'presentation_title', 'created_at', 'recommended_for_publication')
    list_filter = ('conference', 'recommended_for_publication', 'created_at')
    # разрешить редактировать статус прямо из списка
    list_editable = ('recommended_for_publication',)
    search_fields = ('participant__username', 'presentation_title')
    autocomplete_fields = ('participant', 'conference')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'conference', 'rating', 'created_at')
    list_filter = ('conference', 'rating', 'created_at')
    search_fields = ('author__username', 'text')
    autocomplete_fields = ('author', 'conference')
