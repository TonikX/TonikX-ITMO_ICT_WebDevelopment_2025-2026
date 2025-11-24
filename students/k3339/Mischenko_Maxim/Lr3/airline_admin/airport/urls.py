from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r"companies", views.CompanyViewSet)
router.register(r"plane-types", views.PlaneTypeViewSet)
router.register(r"aircrafts", views.AircraftViewSet)
router.register(r"airports", views.AirportViewSet)
router.register(r"crew-members", views.CrewMemberViewSet)
router.register(r"crews", views.CrewViewSet)
router.register(r"crew-assignments", views.CrewAssignmentViewSet)
router.register(r"flights", views.FlightViewSet)
router.register(r"stopovers", views.StopoverViewSet)
router.register(r"crew-permissions", views.CrewMemberFlightPermissionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
