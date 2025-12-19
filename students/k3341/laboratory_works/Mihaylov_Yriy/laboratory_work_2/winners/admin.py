from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Race, RaceRegistration, Comment, Heat, HeatResult


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'race_time']
    list_filter = ['race_time']

@admin.register(RaceRegistration)
class RaceRegistrationAdmin(admin.ModelAdmin):
    list_display = ['race', 'racer', 'registration_time', 'is_confirmed']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['race', 'commentator', 'comment_time', 'comment_type', 'rating']

@admin.register(Heat)
class HeatAdmin(admin.ModelAdmin):
    list_display = ['name', 'race', 'heat_time']
    list_filter = ['race', 'heat_time']
    search_fields = ['name', 'race__name']

@admin.register(HeatResult)
class HeatResultAdmin(admin.ModelAdmin):
    list_display = ['heat', 'racer', 'position']
    list_filter = ['heat__race', 'heat']
    search_fields = ['racer__user__username', 'heat__name']