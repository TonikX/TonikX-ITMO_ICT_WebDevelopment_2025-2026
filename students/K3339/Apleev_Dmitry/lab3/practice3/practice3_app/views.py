from django.shortcuts import render

# Create your views here.

# main/views.py
from rest_framework import viewsets, generics
from rest_framework.decorators import action

from .models import Owner, Car, DriverLicense, Ownership
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    OwnerSerializer, CarSerializer,
    DriverLicenseSerializer, OwnershipSerializer, SimpleOwnerWithCarsSerializer
)
from rest_framework.response import Response

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand', 'model', 'color']

class DriverLicenseViewSet(viewsets.ModelViewSet):
    queryset = DriverLicense.objects.all()
    serializer_class = DriverLicenseSerializer

class OwnershipViewSet(viewsets.ModelViewSet):
    queryset = Ownership.objects.all()
    serializer_class = OwnershipSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    # Добавляем экшн для получения машин владельца
    @action(detail=True, methods=['get'], url_path='cars')
    def get_owner_cars(self, request, pk=None):
        owner = self.get_object()
        cars = Car.objects.filter(ownerships__owner=owner)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

