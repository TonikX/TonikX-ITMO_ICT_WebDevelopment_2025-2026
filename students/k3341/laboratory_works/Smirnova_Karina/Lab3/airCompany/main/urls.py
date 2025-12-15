from django.urls import path, include
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import (
    AirlineCompanyViewSet, PlaneViewSet, CrewViewSet,
    RouteViewSet, FlightViewSet, CrewMemberViewSet, MostPopularPaneType, RoutesBelowCapacity,
    AvailableSeats, PlanesUnderRepair, TotalEmployees, auth_demo
)

class NoGlobalSecuritySchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # schema — объект openapi.Swagger
        # Убираем глобальный security (если он есть)
        # Если присвоить пустой список, Swagger может показать пустую security — лучше удалить ключ:
        try:
            # у OpenAPI объекта атрибут security может быть списком или None
            schema.security = None
        except Exception:
            # на всякий случай: ничего не делаем, если структура неожиданная
            pass
        return schema

router = DefaultRouter()
router.register(r'airline-companies', AirlineCompanyViewSet)
router.register(r'planes', PlaneViewSet)
router.register(r'crews', CrewViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'flights', FlightViewSet)
# router.register(r'transit-landings', TransitLandingViewSet)
router.register(r'crew-members', CrewMemberViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Airlines API",
        default_version='v1',
        description="API for airline management (planes, flights, crews, routes, etc.)",
        contact=openapi.Contact(email="you@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=NoGlobalSecuritySchemaGenerator,
)

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

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('auth-demo/', auth_demo, name='auth-demo'),
]

urlpatterns += [
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]