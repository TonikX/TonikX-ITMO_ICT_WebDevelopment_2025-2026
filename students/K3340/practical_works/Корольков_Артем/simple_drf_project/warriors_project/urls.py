from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ВКЛЮЧАЕМ ПУТИ ПРИЛОЖЕНИЯ БЕЗ ПРЕФИКСА 'war/'
    # Теперь пути из warriors_app будут доступны от корня
    path('', include('warriors_app.urls')),
]