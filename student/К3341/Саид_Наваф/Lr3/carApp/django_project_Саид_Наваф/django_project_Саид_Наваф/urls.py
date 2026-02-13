# project/urls.py (your top-level file)
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Optional: drf-spectacular schema + swagger
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # app API (router from carApp/urls.py)
    path('api/', include('carApp.urls', namespace='carApp')),

    # JWT auth endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Djoser endpoints (registration, users)
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),  # if using djoser jwt helpers

    # Optional: OpenAPI schema and Swagger UI (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]