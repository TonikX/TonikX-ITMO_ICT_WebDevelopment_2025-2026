# carApp/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

app_name = "carApp"   # so include(..., namespace='carApp') works

router = routers.DefaultRouter()
# Register viewsets - adjust names if you used different class names
router.register(r'owners', views.OwnerViewSet, basename='owner')
router.register(r'cars', views.CarViewSet, basename='car')
router.register(r'vehicle-models', views.VehicleModelViewSet, basename='vehiclemodel')
router.register(r'insurance', views.InsurancePolicyViewSet, basename='insurance')
router.register(r'services', views.ServiceRecordViewSet, basename='service')
router.register(r'registrations', views.RegistrationViewSet, basename='registration')
router.register(r'ownerships', views.OwnershipViewSet, basename='ownership')
router.register(r'contacts', views.OwnerContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
]