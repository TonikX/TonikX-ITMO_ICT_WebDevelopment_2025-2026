from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'aircrafts', AircraftViewSet)
router.register(r'airports', AirportViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'crews', CrewViewSet)
router.register(r'crew-members', CrewMemberViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'transit-stops', TransitStopViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('current-user/', views.current_user_info),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]