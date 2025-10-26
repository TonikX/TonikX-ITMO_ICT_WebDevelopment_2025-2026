# blogfspo/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Админ-панель
    path('admin/', admin.site.urls),

    # Включение URL-адресов из приложения automobiles
    path('', include('automobiles.urls')),
]

# Настройки админ-панели
admin.site.site_header = "Система учета автовладельцев"
admin.site.site_title = "Автовладельцы"
admin.site.index_title = "Администрирование системы"