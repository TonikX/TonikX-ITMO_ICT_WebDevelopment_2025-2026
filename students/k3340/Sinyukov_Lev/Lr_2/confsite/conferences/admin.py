from django.contrib import admin
from .models import Topic, Venue, Conference, Registration, Review

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    search_fields = ['name', 'city']

class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0
    fields = ('author', 'talk_title', 'status', 'recommended_for_publication')
    readonly_fields = ()
    can_delete = True

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'venue', 'date_start', 'date_end']
    list_display_links = ['id', 'title']
    list_filter = ['venue', 'topics']
    search_fields = ['title', 'description', 'participation_terms']
    filter_horizontal = ['topics']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['conference', 'author', 'talk_title', 'status', 'recommended_for_publication', 'created_at']
    list_filter = ['status', 'recommended_for_publication', 'conference']
    search_fields = ['talk_title', 'talk_abstract', 'author__username', 'author__email']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['conference', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'conference']
    search_fields = ['text', 'reviewer__username', 'conference__title']
    readonly_fields = ['conf_date_start_snapshot', 'conf_date_end_snapshot']