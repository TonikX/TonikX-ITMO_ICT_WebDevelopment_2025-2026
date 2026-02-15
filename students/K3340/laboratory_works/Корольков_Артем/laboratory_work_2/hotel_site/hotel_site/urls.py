from django.contrib import admin
from django.urls import path, include
from hotels.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotels/', include('hotels.urls')),
    path('', home_page, name='home'),  # Главная страница
]