from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import (
    DriverViewSet, BusTypeViewSet, BusViewSet,
    RouteViewSet, WorkShiftViewSet, ParkReportView
)

router = DefaultRouter()
router.register('drivers', DriverViewSet)
router.register('bus-types', BusTypeViewSet)
router.register('buses', BusViewSet)
router.register('routes', RouteViewSet)
router.register('shifts', WorkShiftViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api/report/park/', ParkReportView.as_view()),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]