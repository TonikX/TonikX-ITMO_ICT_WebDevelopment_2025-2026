from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Car, Ownership
from .forms import OwnerCreateForm
from .models import Car, License, Ownership

User = get_user_model()


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    pass


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = OwnerCreateForm
    model = User

    list_display = [
        'username', 'email', 'last_name', 'first_name', 'birth_date',
        'passport', 'nationality', 'home_address'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'passport']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': (
                'first_name', 'last_name', 'email',
                'birth_date', 'passport', 'home_address', 'nationality'
            )
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'email',
                'first_name', 'last_name', 'birth_date',
                'passport', 'home_address', 'nationality'
            ),
        }),
    )

    ordering = ['last_name', 'first_name']
