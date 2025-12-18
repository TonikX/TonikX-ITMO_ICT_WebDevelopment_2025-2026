from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tax_id = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    contact_info = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    class Unit(models.TextChoices):
        PIECE = "piece", "Piece"
        KG = "kg", "Kilogram"
        TON = "ton", "Ton"

    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, related_name="products"
    )
    unit = models.CharField(max_length=16, choices=Unit.choices)
    shelf_life_days = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.code} — {self.name}"


class BrokerCompany(models.Model):
    name = models.CharField(max_length=255, unique=True)
    monthly_fee = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    contact_info = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Broker(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="broker_profile",
    )
    company = models.ForeignKey(
        BrokerCompany, on_delete=models.CASCADE, related_name="brokers"
    )
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=4, default=Decimal("0.1000")
    )
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Broker {self.id} ({self.company.name})"


class Batch(models.Model):
    number = models.CharField(max_length=128, unique=True)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name="batches")
    contract_date = models.DateField()
    shipment_date = models.DateField(blank=True, null=True)
    prepayment = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-contract_date", "-id"]

    def __str__(self) -> str:
        return self.number


class BatchItem(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="batch_items"
    )
    production_date = models.DateField()
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    unit_price = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["production_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.product.code} in {self.batch.number}"

    @property
    def total_price(self) -> Decimal:
        return (self.quantity or Decimal("0")) * (self.unit_price or Decimal("0"))

    @property
    def is_expired(self) -> bool:
        reference_date = self.batch.shipment_date or self.batch.contract_date
        expiry_date = self.production_date + timedelta(days=self.product.shelf_life_days)
        return reference_date > expiry_date

