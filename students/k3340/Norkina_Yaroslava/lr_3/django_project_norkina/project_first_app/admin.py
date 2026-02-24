from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import User
from .models import DriverLicense
from .models import Car
from .models import Ownership

admin.site.register(DriverLicense)
admin.site.register(Car)
admin.site.register(Ownership)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Личные данные', {'fields': ('birth_date',)}),
        ('Паспортные данные', {'fields': ('passport_number', 'home_address', 'nationality')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Личные данные', {'fields': ('first_name', 'last_name', 'birth_date')}),
        ('Паспортные данные', {'fields': ('passport_number', 'home_address', 'nationality')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'birth_date', 'passport_number')