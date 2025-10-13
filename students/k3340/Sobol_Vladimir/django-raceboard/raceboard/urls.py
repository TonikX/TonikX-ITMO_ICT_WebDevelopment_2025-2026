from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(pattern_name='races:race_list', permanent=False)),
    path('races/', include('races.urls', namespace='races')),
]
