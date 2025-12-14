from django.contrib import admin
from .models import Race, Racer, Registration, Comment


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location']
    list_filter = ['date', 'location']
    search_fields = ['name', 'location', 'description']
    date_hierarchy = 'date'


@admin.register(Racer)
class RacerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'team_name', 'experience', 'racer_class']
    list_filter = ['experience', 'racer_class']
    search_fields = ['full_name', 'team_name']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['racer', 'race', 'race_time', 'result', 'position']
    list_filter = ['race', 'race__date']
    search_fields = ['racer__full_name', 'race__name']
    raw_id_fields = ['racer', 'race']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('racer', 'race')
        }),
        ('Результаты заезда', {
            'fields': ('race_time', 'result', 'position')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'race', 'comment_type', 'rating', 'created_at']
    list_filter = ['comment_type', 'rating', 'created_at']
    search_fields = ['text', 'author__username', 'race__name']
    date_hierarchy = 'created_at'
