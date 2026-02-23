from django.contrib import admin

from .models import Owner, Car, Ownership, DriverLicense

# Регистрируем модели
@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'last_name', 'first_name', 'birth_date', 'passport_number', 'address', 'nationality']

admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(DriverLicense)

