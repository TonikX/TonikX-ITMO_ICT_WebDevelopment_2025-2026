from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NewspaperViewSet, PrintingHouseViewSet, PostOfficeViewSet, DistributionViewSet
)

router = DefaultRouter()
router.register(r'newspapers', NewspaperViewSet, basename='newspaper')
router.register(r'printing-houses', PrintingHouseViewSet, basename='printinghouse')
router.register(r'post-offices', PostOfficeViewSet, basename='postoffice')
router.register(r'distributions', DistributionViewSet, basename='distribution')

urlpatterns = [
    path('', include(router.urls)),
]

