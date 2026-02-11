from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API для нашего приложения
    path('api/', include('review_system.urls')),
    
    # Djoser (Регистрация, логин, токены)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # !!! ДОБАВЬ ВОТ ЭТУ СТРОЧКУ !!!
    # Она включает стандартный вход/выход в веб-интерфейсе
    path('api-auth/', include('rest_framework.urls')), 
]