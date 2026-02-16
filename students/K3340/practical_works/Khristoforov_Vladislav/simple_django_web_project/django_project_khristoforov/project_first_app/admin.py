from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Car, Driving_License, Car_Ownership

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('birth_date', 'passport', 'address', 'nationality')
        }),
    )
   
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('birth_date', 'passport', 'address', 'nationality', 'first_name', 'last_name')
        }),
    )
   
    list_display = ('username', 'first_name', 'last_name', 'birth_date', 'nationality')

admin.site.register(Car)
admin.site.register(Driving_License)
admin.site.register(Car_Ownership)
admin.site.register(User, CustomUserAdmin)