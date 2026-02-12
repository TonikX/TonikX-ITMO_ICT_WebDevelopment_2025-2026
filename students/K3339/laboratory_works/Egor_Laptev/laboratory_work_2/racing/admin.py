from django.contrib import admin
from .models import ParticipantProfile, Car, Race, Registration, Comment


@admin.register(ParticipantProfile)
class ParticipantProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team_name', 'experience_years', 'participant_class')
    search_fields = ('full_name', 'team_name')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__full_name')


class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0
    readonly_fields = ('registered_at',)


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'registrations_count')
    inlines = (RegistrationInline,)
    search_fields = ('title', 'location')
    list_filter = ('date',)
    date_hierarchy = 'date'
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'location', 'date')
        }),
    )
    
    def registrations_count(self, obj):
        return obj.registrations.count()
    registrations_count.short_description = 'Количество регистраций'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('race', 'participant', 'car', 'position', 'finish_time_ms', 'registered_at')
    list_filter = ('race', 'participant__participant_class')
    search_fields = ('participant__full_name', 'race__title', 'participant__team_name')
    list_editable = ('position', 'finish_time_ms')
    fieldsets = (
        ('Регистрация', {
            'fields': ('race', 'participant', 'car', 'registered_at')
        }),
        ('Результаты заезда', {
            'fields': ('position', 'finish_time_ms'),
            'description': 'Укажите позицию участника и время заезда в миллисекундах'
        }),
    )
    readonly_fields = ('registered_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('race', 'commentator', 'comment_type', 'rating', 'created_at')
    list_filter = ('comment_type', 'rating')
