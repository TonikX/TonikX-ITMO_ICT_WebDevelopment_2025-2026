from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet,
    EmployeeViewSet,
    ServiceCategoryViewSet,
    ServiceViewSet,
    OrderViewSet,
    PaymentOrderViewSet,
)

router = DefaultRouter()
router.register(r"clients", ClientViewSet)
router.register(r"employees", EmployeeViewSet)
router.register(r"categories", ServiceCategoryViewSet)
router.register(r"services", ServiceViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"payments", PaymentOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
