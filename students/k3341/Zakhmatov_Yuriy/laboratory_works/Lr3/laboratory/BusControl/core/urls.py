from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    DriverClassViewSet,
    DriverViewSet,
    BusTypeViewSet,
    BusViewSet,
    RouteViewSet,
    WorkShiftViewSet, BusDepotViewSet,
)

router = DefaultRouter()
router.register(r'depots', BusDepotViewSet, basename='depot')
router.register(r'driverclasses', DriverClassViewSet, basename='driverclass')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'bus-types', BusTypeViewSet, basename='bus-type')
router.register(r'buses', BusViewSet, basename='bus')
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'workshifts', WorkShiftViewSet, basename='workshift')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),


    path('', include(router.urls)),
]
