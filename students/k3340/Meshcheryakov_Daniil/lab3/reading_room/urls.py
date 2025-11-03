from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReadingRoomViewSet,
    ReaderViewSet,
    ReservationViewSet,
    LibrarianViewSet,
    ScheduleViewSet,
    QuarterReportView,
)

router = DefaultRouter()
router.register(r"reading-rooms", ReadingRoomViewSet)
router.register(r"readers", ReaderViewSet)
router.register(r"reservations", ReservationViewSet)
router.register(r"librarians", LibrarianViewSet)
router.register(r"schedules", ScheduleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("reports/quarter/", QuarterReportView.as_view(), name="quarter-report"),
]

