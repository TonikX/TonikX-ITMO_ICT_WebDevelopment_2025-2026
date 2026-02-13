from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Поля в списке пользователей
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    
    # Поля в форме редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone', 'address', 'date_of_birth')
        }),
    )
    
    # Поля в форме создания
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('email', 'first_name', 'last_name', 'phone', 'address', 'date_of_birth')
        }),
    )
    
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']

admin.site.register(CustomUser, CustomUserAdmin)