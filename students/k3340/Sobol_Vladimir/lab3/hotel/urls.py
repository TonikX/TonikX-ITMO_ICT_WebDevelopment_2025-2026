from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet,
    ClientViewSet,
    StayViewSet,
    EmployeeViewSet,
    EmployeeScheduleViewSet,
    QuarterReportView,
)

router = DefaultRouter()
router.register(r"rooms", RoomViewSet)
router.register(r"clients", ClientViewSet)
router.register(r"stays", StayViewSet)
router.register(r"employees", EmployeeViewSet)
router.register(r"schedules", EmployeeScheduleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("reports/quarter/", QuarterReportView.as_view(), name="quarter-report"),
]
