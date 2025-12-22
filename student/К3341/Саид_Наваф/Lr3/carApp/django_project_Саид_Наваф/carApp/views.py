# app/views.py
from rest_framework import viewsets
from .models import Owner, Car, VehicleModel, InsurancePolicy, ServiceRecord, Registration, Ownership, OwnerContact
from .serializers import OwnerDetailSerializer, CarListSerializer, VehicleModelSerializer, InsurancePolicySerializer, ServiceRecordSerializer, RegistrationSerializer, OwnershipSerializer, OwnerContactSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by('last_name')
    serializer_class = OwnerDetailSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer

class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer

class InsurancePolicyViewSet(viewsets.ModelViewSet):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer

class ServiceRecordViewSet(viewsets.ModelViewSet):
    queryset = ServiceRecord.objects.all()
    serializer_class = ServiceRecordSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

class OwnershipViewSet(viewsets.ModelViewSet):
    queryset = Ownership.objects.all()
    serializer_class = OwnershipSerializer

class OwnerContactViewSet(viewsets.ModelViewSet):
    queryset = OwnerContact.objects.all()
    serializer_class = OwnerContactSerializer