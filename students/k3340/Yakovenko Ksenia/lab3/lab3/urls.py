from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),

    # главная страница → сразу на API
    path("", RedirectView.as_view(url="/api/", permanent=False)),

    # твой API
    path("api/", include("exchange.api_urls")),
    ]