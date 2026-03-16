from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, CleaningScheduleViewSet, ClientViewSet, EmployeeViewSet


router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'cleaning_schedules', CleaningScheduleViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'Employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]