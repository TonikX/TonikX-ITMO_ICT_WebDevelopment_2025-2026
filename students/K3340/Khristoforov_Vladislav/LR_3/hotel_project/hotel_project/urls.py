from django.contrib import admin
from django.urls import include, path

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/', include('hotel_app.urls')),
   path('auth/', include('djoser.urls')),
   path('auth/', include('djoser.urls.authtoken')),
]
