from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'experience', 'team_name')
    list_filter = ('experience', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('experience', 'driver_class', 'team_name', 'car_description', 'driver_description')
        }),
    )