
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'owners', views.OwnerViewSet)
router.register(r'cars', views.CarViewSet)
router.register(r'licenses', views.DriverLicenseViewSet)
router.register(r'ownerships', views.OwnershipViewSet)

urlpatterns = [
    path('api/', include(router.urls))]