from django.contrib import admin
from .models import (
    Profile, Team, Car, Participant, Race, Registration,
    RaceSession, RaceResult, Comment
)

# -------------------------
# Profile Admin
# -------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    ordering = ('user__username',)


# -------------------------
# Team Admin
# -------------------------
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')


# -------------------------
# Car Admin
# -------------------------
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model',)
    search_fields = ('model',)


# -------------------------
# Participant Admin
# -------------------------
class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('profile', 'participant_class', 'team', 'experience_years', 'created_at')
    list_filter = ('participant_class', 'team')
    search_fields = (
        'profile__user__username',
        'profile__user__first_name',
        'profile__user__last_name',
        'team__name',
    )
    date_hierarchy = 'created_at'
    inlines = [RegistrationInline]


# -------------------------
# Race Admin
# -------------------------
class RaceSessionInline(admin.TabularInline):
    model = RaceSession
    extra = 0

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'date', 'created_by', 'created_at')
    search_fields = ('name', 'location', 'created_by__user__username')
    list_filter = ('date',)
    date_hierarchy = 'date'
    inlines = [RaceSessionInline]


# -------------------------
# RaceSession Admin
# -------------------------
class RaceResultInline(admin.TabularInline):
    model = RaceResult
    extra = 0

@admin.register(RaceSession)
class RaceSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'race', 'order', 'start_time')
    search_fields = ('name', 'race__name')
    list_filter = ('race',)
    inlines = [RaceResultInline]


# -------------------------
# Registration Admin
# -------------------------
class RaceResultInlineForRegistration(admin.TabularInline):
    model = RaceResult
    extra = 0

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'race', 'car', 'created_at')
    search_fields = (
        'participant__profile__user__username',
        'race__name',
        'car__model',
    )
    list_filter = ('race',)
    date_hierarchy = 'created_at'
    inlines = [RaceResultInlineForRegistration]


# -------------------------
# RaceResult Admin
# -------------------------
@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('registration', 'session', 'total_time')
    search_fields = ('registration__participant__profile__user__username', 'session__race__name')
    list_filter = ('session', )


# -------------------------
# Comment Admin
# -------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'race', 'comment_type', 'text', 'created_at')
    list_filter = ('comment_type',)
    search_fields = (
        'profile__user__username',
        'profile__user__first_name',
        'profile__user__last_name',
        'race__name',
        'text'
    )
    date_hierarchy = 'created_at'
