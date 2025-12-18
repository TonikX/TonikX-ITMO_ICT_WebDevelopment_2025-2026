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
router.register(r'hotel-services', views.HotelServiceViewSet)
router.register(r'staff-services', views.StaffServiceViewSet)

urlpatterns = [
    # все роуты API — будут доступны под /api/... (т.к. проект подключает этот файл под префиксом 'api/')
    path('', include(router.urls)),

    # кастомные endpoints (они также будут доступны под /api/)
    path('status/', views.api_status, name='api-status'),
    path('public-sample/', views.public_sample, name='public-sample'),
    path('debug/', views.api_debug, name='api-debug'),
    path('custom-login/', views.custom_token_login, name='custom-login'),
]
