from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from hotels.views import SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('hotels.urls')),
    path('', RedirectView.as_view(pattern_name='hotels_list', permanent=False)),
]
