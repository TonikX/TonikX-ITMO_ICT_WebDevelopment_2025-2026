from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'guests', views.GuestViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'cleaning-schedules', views.CleaningScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reports/', views.ReportView.as_view(), name='reports'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]