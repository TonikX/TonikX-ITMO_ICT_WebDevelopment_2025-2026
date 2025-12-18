"""
URL configuration for library project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


@require_http_methods(["GET"])
def root_view(request):
    """Главная страница API - показывает доступные эндпоинты"""
    return JsonResponse({
        'message': 'Library Management System API',
        'version': '1.0.0',
        'endpoints': {
            'api_documentation': '/api/schema/swagger-ui/',
            'api_schema': '/api/schema/',
            'api_redoc': '/api/schema/redoc/',
            'api_root': '/api/',
            'admin': '/admin/',
        },
        'description': 'Система управления библиотекой - REST API'
    })


urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include('library.urls')),
]

