import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from trading.models import (
    Batch,
    BatchItem,
    Broker,
    BrokerCompany,
    Manufacturer,
    Product,
)


class Command(BaseCommand):
    help = "Populate the database with demo data for reports testing."

    def handle(self, *args, **options):
        self.stdout.write("Creating demo data...")

        # Manufacturers
        acme, _ = Manufacturer.objects.get_or_create(name="Acme Corp")
        globex, _ = Manufacturer.objects.get_or_create(name="Globex Ltd")

        # Products
        oil, _ = Product.objects.get_or_create(
            code="OIL-100",
            defaults={
                "name": "Crude Oil",
                "manufacturer": acme,
                "unit": Product.Unit.TON,
                "shelf_life_days": 90,
            },
        )
        gold, _ = Product.objects.get_or_create(
            code="GOLD-200",
            defaults={
                "name": "Gold Bullion",
                "manufacturer": globex,
                "unit": Product.Unit.KG,
                "shelf_life_days": 365,
            },
        )
        wheat, _ = Product.objects.get_or_create(
            code="WHEAT-300",
            defaults={
                "name": "Wheat",
                "manufacturer": acme,
                "unit": Product.Unit.TON,
                "shelf_life_days": 180,
            },
        )

        # Companies
        prime, _ = BrokerCompany.objects.get_or_create(
            name="Prime Brokers", defaults={"monthly_fee": Decimal("500.00")}
        )
        trust, _ = BrokerCompany.objects.get_or_create(
            name="Trust Brokers", defaults={"monthly_fee": Decimal("400.00")}
        )

        # Users for brokers
        User = get_user_model()
        user_a, _ = User.objects.get_or_create(username="broker_a", defaults={"email": "broker_a@example.com"})
        user_b, _ = User.objects.get_or_create(username="broker_b", defaults={"email": "broker_b@example.com"})
        user_a.set_password("P@ssw0rd")
        user_b.set_password("P@ssw0rd")
        user_a.save()
        user_b.save()

        # Brokers
        broker_a, _ = Broker.objects.get_or_create(
            company=prime, defaults={"commission_rate": Decimal("0.10"), "user": user_a}
        )
        broker_b, _ = Broker.objects.get_or_create(
            company=prime, defaults={"commission_rate": Decimal("0.10"), "user": user_b}
        )
        broker_c, _ = Broker.objects.get_or_create(
            company=trust, defaults={"commission_rate": Decimal("0.10")}
        )

        # Ensure user assignment in case brokers already existed
        if not broker_a.user_id:
            broker_a.user = user_a
            broker_a.save(update_fields=["user"])
        if not broker_b.user_id:
            broker_b.user = user_b
            broker_b.save(update_fields=["user"])

        # Batches
        batch1, _ = Batch.objects.get_or_create(
            number="B001",
            defaults={
                "broker": broker_a,
                "contract_date": datetime.date(2025, 1, 10),
                "shipment_date": datetime.date(2025, 4, 15),
                "prepayment": True,
            },
        )
        batch2, _ = Batch.objects.get_or_create(
            number="B002",
            defaults={
                "broker": broker_b,
                "contract_date": datetime.date(2025, 2, 5),
                "shipment_date": datetime.date(2025, 2, 20),
                "prepayment": False,
            },
        )
        batch3, _ = Batch.objects.get_or_create(
            number="B003",
            defaults={
                "broker": broker_c,
                "contract_date": datetime.date(2025, 3, 1),
                "shipment_date": datetime.date(2025, 3, 10),
                "prepayment": False,
            },
        )
        batch4, _ = Batch.objects.get_or_create(
            number="B004",
            defaults={
                "broker": broker_a,
                "contract_date": datetime.date(2025, 3, 25),
                "shipment_date": datetime.date(2025, 3, 30),
                "prepayment": True,
            },
        )

        # Batch items
        BatchItem.objects.get_or_create(
            batch=batch1,
            product=oil,
            defaults={
                "production_date": datetime.date(2024, 12, 1),
                "quantity": Decimal("100"),
                "unit_price": Decimal("50.00"),
            },
        )
        BatchItem.objects.get_or_create(
            batch=batch2,
            product=gold,
            defaults={
                "production_date": datetime.date(2025, 1, 15),
                "quantity": Decimal("10"),
                "unit_price": Decimal("2000.00"),
            },
        )
        BatchItem.objects.get_or_create(
            batch=batch3,
            product=wheat,
            defaults={
                "production_date": datetime.date(2025, 2, 1),
                "quantity": Decimal("500"),
                "unit_price": Decimal("2.00"),
            },
        )
        BatchItem.objects.get_or_create(
            batch=batch4,
            product=oil,
            defaults={
                "production_date": datetime.date(2025, 3, 1),
                "quantity": Decimal("70"),
                "unit_price": Decimal("55.00"),
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo data created."))

