from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from rest_framework.response import Response

class FuelReference(models.Model):
    id_kind_fuel = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40)
    burning_temp = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=40)
    density = models.DecimalField(max_digits=10, decimal_places=2)
    season = models.IntegerField()
    percent_sulfur = models.DecimalField(max_digits=5, decimal_places=2)
    min_usage_temp = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "fuel_reference"


class Companies(models.Model):
    id_company = models.AutoField(primary_key=True)
    type_company = models.IntegerField()
    legal_address = models.CharField(max_length=100)
    company_title = models.CharField(max_length=100)

    class Meta:
        db_table = "companies"


class ProducedFuel(models.Model):
    id_produced_fuel = models.AutoField(primary_key=True)
    id_kind_fuel = models.ForeignKey(
        FuelReference,
        on_delete=models.CASCADE,
        db_column="id_kind_fuel"
    )
    id_company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        db_column="id_company"
    )

    class Meta:
        db_table = "produced_fuel"


class GasStation(models.Model):
    id_station = models.AutoField(primary_key=True)
    id_company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        db_column="id_company"
    )
    station_address = models.CharField(max_length=100)

    class Meta:
        db_table = "gas_station"


class User(AbstractUser):
    id_station = models.ForeignKey(
        GasStation,
        on_delete=models.CASCADE,
        related_name="users"
    )

    REQUIRED_FIELDS = ['id_station']

    class Meta:
        db_table = "users"


class SoldFuel(models.Model):
    id_sold_fuel = models.AutoField(primary_key=True)
    id_produced_fuel = models.ForeignKey(
        ProducedFuel,
        on_delete=models.CASCADE,
        db_column="id_produced_fuel"
    )
    id_station = models.ForeignKey(
        GasStation,
        on_delete=models.CASCADE,
        db_column="id_station"
    )

    class Meta:
        db_table = "sold_fuel"


class FuelPrices(models.Model):
    id_fuel_price = models.AutoField(primary_key=True)
    id_sold_fuel = models.ForeignKey(
        SoldFuel,
        on_delete=models.CASCADE,
        db_column="id_sold_fuel"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    per_liter = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "fuel_prices"

    @staticmethod
    def getById(target_id):
        try:
            price = FuelPrices.objects.get(id_fuel_price=target_id)
        except FuelPrices.DoesNotExist:
            return Response({"detail": "Price not found"}, status=404)
        
        now = timezone.now()

        # Проверка активности цены
        if price.start_time > now or (price.end_time and price.end_time <= now):
            return Response({"detail": "Price is not active"}, status=400)

        return price



class Clients(models.Model):
    id_client = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    patronymic = models.CharField(max_length=40)
    phone_number = models.BigIntegerField()
    address = models.CharField(max_length=100)

    class Meta:
        db_table = "clients"


class ClientCards(models.Model):
    id_card = models.AutoField(primary_key=True)
    id_company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        db_column="id_company"
    )
    id_client = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        db_column="id_client"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rub = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "client_cards"
    
    @staticmethod
    def getById(target_id):
        try:
            card = ClientCards.objects.get(id_card=target_id)
        except ClientCards.DoesNotExist:
            return Response({"detail": "Card not found"}, status=404)
        
        now = timezone.now().date()  # сравниваем только даты

        # Проверка активности карты
        if card.start_date > now or (card.end_date and card.end_date <= now):
            return Response({"detail": "Card is not active"}, status=400)

        return card


class Sales(models.Model):
    id_sales = models.BigAutoField(primary_key=True)
    id_fuel_price = models.ForeignKey(
        FuelPrices,
        on_delete=models.CASCADE,
        db_column="id_fuel_price"
    )
    id_card = models.ForeignKey(
        ClientCards,
        on_delete=models.CASCADE,
        db_column="id_card"
    )
    sale_date = models.DateTimeField()
    sold_liters_volume = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "sales"
