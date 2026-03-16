from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NewspaperViewSet, PrintingHouseViewSet, PostOfficeViewSet, DistributionViewSet
)
from .auth_views import get_auth_token

router = DefaultRouter()
router.register(r'newspapers', NewspaperViewSet, basename='newspaper')
router.register(r'printing-houses', PrintingHouseViewSet, basename='printinghouse')
router.register(r'post-offices', PostOfficeViewSet, basename='postoffice')
router.register(r'distributions', DistributionViewSet, basename='distribution')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/get-token/', get_auth_token, name='get-auth-token'),
]

