from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    BatchItemViewSet,
    BatchViewSet,
    BrokerCompanyViewSet,
    BrokerViewSet,
    BrokerSalariesView,
    ExpiredItemsView,
    LatestTradesReportView,
    ManufacturerViewSet,
    ProductViewSet,
    ProductQuantityByDateView,
    ProductsNeverSoldByCompanyView,
    TopManufacturerRevenueView,
)

router = DefaultRouter()
router.register(r"manufacturers", ManufacturerViewSet)
router.register(r"products", ProductViewSet)
router.register(r"broker-companies", BrokerCompanyViewSet)
router.register(r"brokers", BrokerViewSet)
router.register(r"batches", BatchViewSet)
router.register(r"batch-items", BatchItemViewSet)

urlpatterns = [
    path("reports/product-quantities/", ProductQuantityByDateView.as_view()),
    path("reports/top-manufacturer/", TopManufacturerRevenueView.as_view()),
    path("reports/unsold-products/", ProductsNeverSoldByCompanyView.as_view()),
    path("reports/expired-items/", ExpiredItemsView.as_view()),
    path("reports/broker-salaries/", BrokerSalariesView.as_view()),
    path("reports/latest-trades/", LatestTradesReportView.as_view()),
]

urlpatterns += router.urls

