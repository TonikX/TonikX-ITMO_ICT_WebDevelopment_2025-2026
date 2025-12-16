from rest_framework import generics
from .models import Owner, Car, Ownership
from .serializers import (
    OwnerSerializer,
    CarSerializer,
    OwnershipSerializer,
)


class OwnerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OwnerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class OwnershipListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ownership.objects.all()
    serializer_class = OwnershipSerializer


class OwnershipRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ownership.objects.all()
    serializer_class = OwnershipSerializer


class CarsByOwnerAPIView(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        owner_id = self.kwargs["owner_id"]
        return Car.objects.filter(ownerships__owner_id=owner_id).distinct()


class OwnersByCarAPIView(generics.ListAPIView):
    serializer_class = OwnerSerializer

    def get_queryset(self):
        car_id = self.kwargs["car_id"]
        return Owner.objects.filter(ownerships__car_id=car_id).distinct()
