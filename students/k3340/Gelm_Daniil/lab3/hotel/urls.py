from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet, GuestViewSet, StayViewSet,
    EmployeeViewSet, CleaningScheduleViewSet
)

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'guests', GuestViewSet, basename='guest')
router.register(r'stays', StayViewSet, basename='stay')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'cleaning-schedules', CleaningScheduleViewSet, basename='cleaning-schedule')

urlpatterns = [
    path('api/', include(router.urls)),
]

