from django.urls import path, include
from rest_framework import routers
from .views import PatientViewSet, DoctorViewSet, VisitViewSet, PaymentViewSet, RoomViewSet, DoctorScheduleViewSet

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'schedules', DoctorScheduleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
