from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    # Auth endpoints (Djoser token)
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    # Domain APIs
    path("api/", include(("drones.urls", "drones"), namespace="drones")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
