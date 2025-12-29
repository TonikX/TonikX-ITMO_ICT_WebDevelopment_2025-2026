from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import (
    FuelReference, Companies, ProducedFuel, GasStation, User,
    SoldFuel, FuelPrices, Clients, ClientCards, Sales
)


class FuelReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelReference
        fields = "__all__"

class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = "__all__"

class ProducedFuelSerializer(serializers.ModelSerializer):
    fuel = FuelReferenceSerializer(source="id_kind_fuel", read_only=True)
    company = CompaniesSerializer(source="id_company", read_only=True)

    id_kind_fuel = serializers.PrimaryKeyRelatedField(
        queryset=FuelReference.objects.all(),
        write_only=True
    )
    id_company = serializers.PrimaryKeyRelatedField(
        queryset=Companies.objects.all(),
        write_only=True
    )

    class Meta:
        model = ProducedFuel
        fields = (
            "id_produced_fuel",
            "fuel",
            "company",
            "id_kind_fuel",
            "id_company",
        )

class GasStationSerializer(serializers.ModelSerializer):
    company = CompaniesSerializer(source="id_company", read_only=True)
    id_company = serializers.PrimaryKeyRelatedField(
        queryset=Companies.objects.all(),
        write_only=True
    )

    class Meta:
        model = GasStation
        fields = (
            "id_station",
            "station_address",
            "company",
            "id_company",
        )

class SoldFuelSerializer(serializers.ModelSerializer):
    produced_fuel = ProducedFuelSerializer(
        source="id_produced_fuel",
        read_only=True
    )
    station = GasStationSerializer(
        source="id_station",
        read_only=True
    )

    id_produced_fuel = serializers.PrimaryKeyRelatedField(
        queryset=ProducedFuel.objects.all(),
        write_only=True
    )
    id_station = serializers.PrimaryKeyRelatedField(
        queryset=GasStation.objects.all(),
        write_only=True
    )

    class Meta:
        model = SoldFuel
        fields = (
            "id_sold_fuel",
            "produced_fuel",
            "station",
            "id_produced_fuel",
            "id_station",
        )

class FuelPricesSerializer(serializers.ModelSerializer):
    sold_fuel = SoldFuelSerializer(
        source="id_sold_fuel",
        read_only=True
    )
    id_sold_fuel = serializers.PrimaryKeyRelatedField(
        queryset=SoldFuel.objects.all(),
        write_only=True
    )

    class Meta:
        model = FuelPrices
        fields = (
            "id_fuel_price",
            "sold_fuel",
            "id_sold_fuel",
            "start_time",
            "end_time",
            "per_liter",
        )

class ClientCardsSerializer(serializers.ModelSerializer):
    client = ClientsSerializer(source="id_client", read_only=True)
    company = CompaniesSerializer(source="id_company", read_only=True)

    id_client = serializers.PrimaryKeyRelatedField(
        queryset=Clients.objects.all(),
        write_only=True
    )
    id_company = serializers.PrimaryKeyRelatedField(
        queryset=Companies.objects.all(),
        write_only=True
    )

    class Meta:
        model = ClientCards
        fields = (
            "id_card",
            "client",
            "company",
            "id_client",
            "id_company",
            "start_date",
            "end_date",
            "balance",
            "discount_percent",
            "discount_rub",
        )

class SalesSerializer(serializers.ModelSerializer):
    fuel_price = FuelPricesSerializer(
        source="id_fuel_price",
        read_only=True
    )
    card = ClientCardsSerializer(
        source="id_card",
        read_only=True
    )

    id_fuel_price = serializers.PrimaryKeyRelatedField(
        queryset=FuelPrices.objects.all(),
        write_only=True
    )
    id_card = serializers.PrimaryKeyRelatedField(
        queryset=ClientCards.objects.all(),
        write_only=True
    )

    class Meta:
        model = Sales
        fields = (
            "id_sales",
            "fuel_price",
            "card",
            "id_fuel_price",
            "id_card",
            "sale_date",
            "sold_liters_volume",
        )

class CustomUserCreateSerializer(UserCreateSerializer):
    id_station = serializers.PrimaryKeyRelatedField(
        queryset=GasStation.objects.all(),
        required=True,
        allow_null=False
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "username",
            "password",
            "re_password",
            "email",
            "id_station",
        )

class CustomUserSerializer(UserSerializer):
    gas_station = GasStationSerializer(
        source="id_station",
        read_only=True
    )

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ("gas_station",)

class PaymentCalculationSerializer(serializers.Serializer):
    id_card = serializers.IntegerField()
    initial_amount = serializers.FloatField(min_value=0)

class PaymentCalculationResultSerializer(serializers.Serializer):
    final_amount = serializers.FloatField()
    sufficient_balance = serializers.BooleanField()

class FuelPurchaseCalculationSerializer(serializers.Serializer):
    id_fuel_price = serializers.IntegerField()
    liters = serializers.FloatField(min_value=0)
    id_card = serializers.IntegerField(required=False)
