from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet, GuestViewSet, LivingRecordViewSet,
    StaffViewSet, CleaningScheduleViewSet, FloorViewSet, CleaningRecordViewSet,
    hotel_quarterly_report
)

router = DefaultRouter()
router.register(r'room', RoomViewSet, basename='room')
router.register(r'guest', GuestViewSet, basename='guest')
router.register(r'living_record', LivingRecordViewSet, basename='living_record')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'cleaning_schedule', CleaningScheduleViewSet, basename='cleaning_schedule')
router.register(r'floor', FloorViewSet, basename='floor')
router.register(r'cleaning_record', CleaningRecordViewSet, basename='cleaning_record')

urlpatterns = [
    path('', include(router.urls)),
    path('report/quarterly/', hotel_quarterly_report, name='hotel-quarterly-report'),
]