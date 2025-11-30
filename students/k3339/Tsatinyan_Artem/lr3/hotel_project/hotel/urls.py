from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RoomViewSet,
    ClientViewSet,
    EmployeeViewSet,
    CleaningScheduleViewSet,
    StayViewSet,
    ClientsInRoomView,
    ClientsFromCityCountView,
    CleanerForClientView,
    FreeRoomsView,
    ClientsSameDaysView,
    QuarterReportView,
)

router = DefaultRouter()
router.register("rooms", RoomViewSet)
router.register("clients", ClientViewSet)
router.register("employees", EmployeeViewSet)
router.register("schedules", CleaningScheduleViewSet)
router.register("stays", StayViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("reports/clients-in-room/", ClientsInRoomView.as_view()),
    path("reports/clients-from-city/", ClientsFromCityCountView.as_view()),
    path("reports/cleaner-for-client/", CleanerForClientView.as_view()),
    path("reports/free-rooms/", FreeRoomsView.as_view()),
    path("reports/clients-same-days/", ClientsSameDaysView.as_view()),
    path("reports/quarter/", QuarterReportView.as_view()),
]
