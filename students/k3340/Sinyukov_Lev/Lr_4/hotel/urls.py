from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet,
    ClientViewSet,
    StayViewSet,
    EmployeeViewSet,
    CleaningScheduleViewSet,
)

router = DefaultRouter()
router.register("rooms", RoomViewSet)
router.register("clients", ClientViewSet)
router.register("stays", StayViewSet)
router.register("employees", EmployeeViewSet)
router.register("schedules", CleaningScheduleViewSet)

urlpatterns = router.urls