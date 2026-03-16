from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Race, Registration, Comment

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Данные гонщика (ЛР)', {'fields': ('bio', 'experience', 'racer_class')}),
    )

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('race', 'user', 'team_name', 'result_place', 'race_time')
    list_filter = ('race', 'team_name')
    list_editable = ('result_place', 'race_time')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Race)
admin.site.register(Comment)