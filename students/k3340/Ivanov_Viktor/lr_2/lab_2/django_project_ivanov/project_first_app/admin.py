from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Avtomobil, Vladenie, Voditelskoe_udostoverenie


# Кастомная админка для расширенной модели пользователя
class CustomUserAdmin(BaseUserAdmin):
    """Админка для расширенной модели User"""
    
    # Поля для отображения в списке
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'nationality', 'is_staff')
    
    # Добавляем новые поля в разделы админки
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('patronymic', 'data_rozhdeniya', 'passport_number', 'home_address', 'nationality')
        }),
    )
    
    # Поля для создания нового пользователя
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('first_name', 'last_name', 'patronymic', 'data_rozhdeniya', 
                      'passport_number', 'home_address', 'nationality', 'email')
        }),
    )


# Регистрируем модели в админ-панели
admin.site.register(User, CustomUserAdmin)
admin.site.register(Avtomobil)
admin.site.register(Vladenie)
admin.site.register(Voditelskoe_udostoverenie)
