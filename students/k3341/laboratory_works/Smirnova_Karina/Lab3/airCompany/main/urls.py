from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AirlineCompanyViewSet, PlaneViewSet, CrewViewSet,
    RouteViewSet, FlightViewSet, TransitLandingViewSet, CrewMemberViewSet, MostPopularPaneType, RoutesBelowCapacity,
    AvailableSeats, PlanesUnderRepair, TotalEmployees
)

router = DefaultRouter()
router.register(r'airline-companies', AirlineCompanyViewSet)
router.register(r'planes', PlaneViewSet)
router.register(r'crews', CrewViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'transit-landings', TransitLandingViewSet)
router.register(r'crew-members', CrewMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Выбрать марку самолета, которая чаще всего летает по маршруту.
    path('most_popular_plane_type/<int:route_id>/', MostPopularPaneType.as_view(), name='most_popular_plane_type'),

    # Выбрать маршрут/маршруты, по которым летают рейсы, заполненные менее чем на XX%
    path('routes_below_capacity/<str:percentage>/', RoutesBelowCapacity.as_view(), name='routes_below_capacity'),

    # Определить наличие свободных мест на заданный рейс.
    path('available_seats/<int:flight_id>/', AvailableSeats.as_view(), name='available_seats'),

    # Определить количество самолетов, находящихся в ремонте.
    path('planes_under_repair/', PlanesUnderRepair.as_view(), name='planes_under_repair'),

    # Определить количество работников компания-авиаперевозчика.
    path('total_employees/<int:company_id>/', TotalEmployees.as_view(), name='total_employees'),
]