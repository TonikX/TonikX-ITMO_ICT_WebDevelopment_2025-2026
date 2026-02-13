from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Team, Car, Race, RaceRegistration, RaceComment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Racer Information', {
            'fields': ('passport_number', 'home_address', 'nationality', 'date_of_birth', 
                      'racing_experience', 'racing_class')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Racer Information', {
            'fields': ('passport_number', 'home_address', 'nationality', 'date_of_birth', 
                      'racing_experience', 'racing_class', 'email', 'first_name', 'last_name')
        }),
    )
    
    list_display = ['username', 'first_name', 'last_name', 'racing_class', 'racing_experience', 'is_staff']
    list_filter = ['racing_class', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'founded_date']
    search_fields = ['name']
    list_filter = ['founded_date']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'brand', 'model', 'team', 'max_speed', 'engine_power']
    search_fields = ['license_plate', 'brand', 'model', 'team__name']
    list_filter = ['team', 'brand']

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'race_type', 'location', 'date']
    search_fields = ['name', 'location']
    list_filter = ['race_type', 'date']
    date_hierarchy = 'date'

@admin.register(RaceRegistration)
class RaceRegistrationAdmin(admin.ModelAdmin):
    list_display = ['racer', 'car', 'race', 'final_position', 'lap_time', 'dnf']
    list_filter = ['race', 'dnf', 'registration_date']
    search_fields = ['racer__first_name', 'racer__last_name', 'car__brand', 'car__model']
    readonly_fields = ['registration_date']
    
    # Admin can set race results
    fieldsets = (
        (None, {
            'fields': ('racer', 'car', 'race', 'registration_date')
        }),
        ('Race Results', {
            'fields': ('lap_time', 'final_position', 'completed_laps', 'dnf')
        }),
    )

@admin.register(RaceComment)
class RaceCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'race', 'comment_type', 'rating', 'created_date']
    list_filter = ['comment_type', 'rating', 'created_date']
    search_fields = ['author__first_name', 'author__last_name', 'race__name', 'text']
    readonly_fields = ['created_date']