from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

class FuelReferenceViewSet(ModelViewSet):
    queryset = FuelReference.objects.all()
    serializer_class = FuelReferenceSerializer

class CompaniesViewSet(ModelViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer

class ProducedFuelViewSet(ModelViewSet):
    queryset = ProducedFuel.objects.select_related(
        "id_kind_fuel", "id_company"
    )
    serializer_class = ProducedFuelSerializer

class GasStationViewSet(ModelViewSet):
    queryset = GasStation.objects.select_related("id_company")
    serializer_class = GasStationSerializer

class SoldFuelViewSet(ModelViewSet):
    queryset = SoldFuel.objects.select_related(
        "id_produced_fuel", "id_station"
    )
    serializer_class = SoldFuelSerializer

class FuelPricesViewSet(ModelViewSet):
    queryset = FuelPrices.objects.select_related("id_sold_fuel")
    serializer_class = FuelPricesSerializer

class ClientsViewSet(ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer

class ClientCardsViewSet(ModelViewSet):
    queryset = ClientCards.objects.select_related(
        "id_client", "id_company"
    )
    serializer_class = ClientCardsSerializer

class SalesViewSet(ModelViewSet):
    queryset = Sales.objects.select_related(
        "id_fuel_price", "id_card"
    )
    serializer_class = SalesSerializer
