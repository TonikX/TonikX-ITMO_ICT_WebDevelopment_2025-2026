from django.contrib import admin
from .models import CarOwner, Car, Ownership, DriversLicense

# Регистрируем владельца авто
admin.site.register(CarOwner)

# Регистрируем остальные таблицы модели данных
admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(DriversLicense)