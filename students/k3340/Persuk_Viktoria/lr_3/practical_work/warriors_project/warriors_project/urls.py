from django.contrib import admin
from django.urls import path, include
from warriors_app.views import ProfessionCreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('war/', include('warriors_app.urls')),
]
