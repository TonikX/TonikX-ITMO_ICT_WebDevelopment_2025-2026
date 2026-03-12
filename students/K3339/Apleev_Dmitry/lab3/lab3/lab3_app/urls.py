from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'cleaningschedules', views.CleaningScheduleViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Hotel API",
        default_version='v1',
        description="API для управления данными гостиницы",
        contact=openapi.Contact(email="admin@hotel.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]