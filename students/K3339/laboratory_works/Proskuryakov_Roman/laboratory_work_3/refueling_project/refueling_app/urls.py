from rest_framework.routers import DefaultRouter
from .views import *

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

urlpatterns = router.urls
