from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'room-types', views.RoomTypeViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'staff', views.StaffViewSet)
router.register(r'cleaning-schedule', views.CleaningScheduleViewSet)
router.register(r'stays', views.StayViewSet)

urlpatterns = [
    path('', include(router.urls)),
]