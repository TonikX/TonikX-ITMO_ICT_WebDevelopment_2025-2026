from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AirlineCompanyViewSet, PlaneViewSet, CrewViewSet,
    RouteViewSet, FlightViewSet, TransitLandingViewSet, CrewMemberViewSet
)

router = DefaultRouter()
router.register(r'airline-companies', AirlineCompanyViewSet)
router.register(r'planes', PlaneViewSet)
router.register(r'crews', CrewViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'transit-landings', TransitLandingViewSet)
router.register(r'crew-members', CrewMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
]