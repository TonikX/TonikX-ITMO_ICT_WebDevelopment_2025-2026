from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    FloorViewSet, RoomViewSet, ClientViewSet, StayRecordViewSet,
    EmployeeViewSet, CleaningScheduleViewSet, CleaningRecordViewSet
)

router = DefaultRouter()
router.register('floors', FloorViewSet)
router.register('rooms', RoomViewSet)
router.register('clients', ClientViewSet)
router.register('stay-records', StayRecordViewSet)
router.register('employees', EmployeeViewSet)
router.register('cleaning-schedules', CleaningScheduleViewSet)
router.register('cleaning-records', CleaningRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
