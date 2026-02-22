from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bus-types', views.BusTypeViewSet)
router.register(r'buses', views.BusViewSet)
router.register(r'routes', views.RouteViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'absences', views.AbsenceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('drivers-on-route/<int:route_id>/', views.drivers_on_route, name='drivers_on_route'),
    path('route-times/', views.route_times, name='route_times'),
    path('total-route-length/', views.total_route_length, name='total_route_length'),
    path('absent-buses/', views.absent_buses, name='absent_buses'),
    path('drivers-by-class/', views.drivers_by_class, name='drivers_by_class'),
    path('fleet-report/', views.fleet_report, name='fleet_report'),
]
