from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BusTypeViewSet,
    BusViewSet,
    RouteViewSet,
    DriverViewSet,
    DriverAssignmentViewSet,
    BusStatusViewSet,
    RouteDriversAPIView,
    TotalRouteLengthAPIView,
    NotActiveBusesAPIView,
    DriverClassStatsAPIView,
    ReportAPIView,
)

router = DefaultRouter()
router.register('bus-types', BusTypeViewSet)
router.register('buses', BusViewSet)
router.register('routes', RouteViewSet)
router.register('drivers', DriverViewSet)
router.register('driver-assignments', DriverAssignmentViewSet)
router.register('bus-statuses', BusStatusViewSet)

urlpatterns = [
    path('routes/<int:route_id>/drivers/', RouteDriversAPIView.as_view()),
    path('routes/total-length/', TotalRouteLengthAPIView.as_view()),
    path('buses/not-active/', NotActiveBusesAPIView.as_view()),
    path('drivers/class-stats', DriverClassStatsAPIView.as_view()),
    path('report/', ReportAPIView.as_view()),
    path('', include(router.urls)),
]
