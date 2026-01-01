from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path

app_name = 'refueling_app'

router = DefaultRouter()
router.register("fuel-reference", FuelReferenceViewSet)
router.register("companies", CompaniesViewSet)
router.register("produced-fuel", ProducedFuelViewSet)
router.register("gas-stations", GasStationViewSet)
router.register("sold-fuel", SoldFuelViewSet)
router.register("fuel-prices", FuelPricesViewSet)
router.register("clients", ClientsViewSet)
router.register("client-cards", ClientCardsViewSet)
router.register("sales", SalesViewSet)

urlpatterns = [
    path("my-station-prices/", FuelPricesByStationView.as_view(), name="my_station_prices"),
    path("calculate-payment/", PaymentCalculationView.as_view(), name="calculate_payment"),
    path("execute-fuel-payment/", FuelPaymentExecuteView.as_view(), name="execute_fuel_payment"),
]

urlpatterns += router.urls
