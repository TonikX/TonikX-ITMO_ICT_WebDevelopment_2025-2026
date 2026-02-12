from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'room-types', RoomTypeViewSet)
router.register(r'floors', FloorViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'guests', GuestViewSet)
router.register(r'stays', StayViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'cleaning', CleaningScheduleViewSet)

urlpatterns = router.urls
