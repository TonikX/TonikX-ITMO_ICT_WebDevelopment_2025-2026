"""
URL configuration for drones application using DRF nested routers.
"""
from rest_framework_nested import routers

from .views import DroneViewSet, FlightViewSet, FlightLogViewSet, DocumentViewSet

router = routers.DefaultRouter()
router.register(r"drones", DroneViewSet, basename="drone")
router.register(r"flights", FlightViewSet, basename="flight")
router.register(r"logs", FlightLogViewSet, basename="log")
router.register(r"documents", DocumentViewSet, basename="document")

drones_router = routers.NestedDefaultRouter(router, r"drones", lookup="drone")
drones_router.register(r"flights", FlightViewSet, basename="drone-flights")
drones_router.register(r"documents", DocumentViewSet, basename="drone-documents")

flights_router = routers.NestedDefaultRouter(router, r"flights", lookup="flight")
flights_router.register(r"logs", FlightLogViewSet, basename="flight-logs")

app_name = "drones"

urlpatterns = (
    router.urls
    + drones_router.urls
    + flights_router.urls
)
