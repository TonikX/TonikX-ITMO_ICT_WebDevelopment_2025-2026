from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FloorViewSet, RoomViewSet, ClientViewSet, StayRecordViewSet,
    EmployeeViewSet, CleaningScheduleViewSet, CleaningRecordViewSet,
    HotelReportView
)

router = DefaultRouter()
router.register("floors", FloorViewSet)
router.register("rooms", RoomViewSet)
router.register("clients", ClientViewSet)
router.register("stay-records", StayRecordViewSet)
router.register("employees", EmployeeViewSet)
router.register("cleaning-schedules", CleaningScheduleViewSet)
router.register("cleaning-records", CleaningRecordViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("hotel-report/", HotelReportView.as_view(), name="hotel-report"),
]
