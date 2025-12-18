from datetime import date
from decimal import Decimal

from django.db.models import DecimalField, ExpressionWrapper, F, Q, Sum
from django.utils.dateparse import parse_date
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Batch, BatchItem, Broker, BrokerCompany, Manufacturer, Product
from .permissions import IsAdminOnly, IsAdminOrBroker, IsAdminOrReadOnly
from .serializers import (
    BatchItemSerializer,
    BatchSerializer,
    BrokerCompanySerializer,
    BrokerSerializer,
    ManufacturerSerializer,
    ProductSerializer,
)


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("manufacturer").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class BrokerCompanyViewSet(viewsets.ModelViewSet):
    queryset = BrokerCompany.objects.all()
    serializer_class = BrokerCompanySerializer
    permission_classes = [IsAdminOrReadOnly]


class BrokerViewSet(viewsets.ModelViewSet):
    queryset = Broker.objects.select_related("company").all()
    serializer_class = BrokerSerializer
    permission_classes = [IsAdminOnly]


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.select_related("broker", "broker__company").all()
    serializer_class = BatchSerializer
    permission_classes = [IsAdminOrBroker]

    def get_queryset(self):
        qs = Batch.objects.select_related("broker", "broker__company")
        user = self.request.user
        if user.is_staff:
            return qs.all()
        broker = getattr(user, "broker_profile", None)
        if broker:
            return qs.filter(broker=broker)
        return qs.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
            return
        broker = getattr(user, "broker_profile", None)
        if not broker:
            raise PermissionDenied("Broker profile is required.")
        serializer.save(broker=broker)

    def perform_update(self, serializer):
        user = self.request.user
        instance: Batch = self.get_object()
        if user.is_staff:
            serializer.save()
            return
        broker = getattr(user, "broker_profile", None)
        if instance.broker_id != getattr(broker, "id", None):
            raise PermissionDenied("You cannot modify batches of other brokers.")
        serializer.save(broker=broker)


class BatchItemViewSet(viewsets.ModelViewSet):
    queryset = BatchItem.objects.select_related(
        "batch",
        "batch__broker",
        "batch__broker__company",
        "product",
        "product__manufacturer",
    ).all()
    serializer_class = BatchItemSerializer
    permission_classes = [IsAdminOrBroker]

    def get_queryset(self):
        qs = BatchItem.objects.select_related(
            "batch",
            "batch__broker",
            "batch__broker__company",
            "product",
            "product__manufacturer",
        )
        user = self.request.user
        if user.is_staff:
            return qs.all()
        broker = getattr(user, "broker_profile", None)
        if broker:
            return qs.filter(batch__broker=broker)
        return qs.none()

    def perform_create(self, serializer):
        user = self.request.user
        batch = serializer.validated_data.get("batch")
        if user.is_staff:
            serializer.save()
            return
        broker = getattr(user, "broker_profile", None)
        if not broker:
            raise PermissionDenied("Broker profile is required.")
        if batch.broker_id != broker.id:
            raise PermissionDenied("You can only add items to your own batches.")
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        instance: BatchItem = self.get_object()
        if user.is_staff:
            serializer.save()
            return
        broker = getattr(user, "broker_profile", None)
        if instance.batch.broker_id != getattr(broker, "id", None):
            raise PermissionDenied("You cannot modify items of other brokers.")
        batch = serializer.validated_data.get("batch", instance.batch)
        if batch.broker_id != broker.id:
            raise PermissionDenied("You can only move items within your batches.")
        serializer.save()


class ProductQuantityByDateView(APIView):
    permission_classes = [IsAdminOrBroker]

    def get(self, request):
        cutoff_raw = request.query_params.get("date")
        cutoff = parse_date(cutoff_raw) if cutoff_raw else None
        qs = BatchItem.objects.all()
        if cutoff:
            qs = qs.filter(batch__contract_date__lte=cutoff)

        aggregated = (
            qs.values("product_id", "product__code", "product__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("product__name")
        )
        return Response(list(aggregated))


class TopManufacturerRevenueView(APIView):
    permission_classes = [IsAdminOrBroker]

    def get(self, request):
        start_raw = request.query_params.get("start")
        end_raw = request.query_params.get("end")
        start_date = parse_date(start_raw) if start_raw else None
        end_date = parse_date(end_raw) if end_raw else None

        price_expr = ExpressionWrapper(
            F("quantity") * F("unit_price"),
            output_field=DecimalField(max_digits=24, decimal_places=2),
        )

        qs = BatchItem.objects.all()
        if start_date:
            qs = qs.filter(batch__contract_date__gte=start_date)
        if end_date:
            qs = qs.filter(batch__contract_date__lte=end_date)

        revenue_by_manufacturer = (
            qs.values("product__manufacturer_id", "product__manufacturer__name")
            .annotate(revenue=Sum(price_expr))
            .order_by("-revenue")
        )
        top = revenue_by_manufacturer.first()
        return Response(top or {}, status=status.HTTP_200_OK)


class ProductsNeverSoldByCompanyView(APIView):
    permission_classes = [IsAdminOrBroker]

    def get(self, request):
        company_id = request.query_params.get("company_id")
        company_name = request.query_params.get("company_name")
        if not company_id and not company_name:
            return Response(
                {"detail": "company_id or company_name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        company_filter: dict[str, object] = {}
        if company_id:
            company_filter["batch__broker__company_id"] = company_id
        if company_name:
            company_filter["batch__broker__company__name"] = company_name

        listed_products = (
            BatchItem.objects.filter(**company_filter)
            .values_list("product_id", flat=True)
            .distinct()
        )
        products = (
            Product.objects.exclude(id__in=listed_products)
            .values("id", "code", "name")
            .order_by("name")
        )
        return Response(list(products))


class ExpiredItemsView(APIView):
    permission_classes = [IsAdminOrBroker]

    def get(self, request):
        items = BatchItem.objects.select_related(
            "product", "product__manufacturer", "batch", "batch__broker", "batch__broker__company"
        ).all()
        expired = [
            {
                "batch_number": item.batch.number,
                "product_code": item.product.code,
                "product_name": item.product.name,
                "broker_id": item.batch.broker_id,
                "broker_company": item.batch.broker.company.name,
            }
            for item in items
            if item.is_expired
        ]
        return Response(expired)


class BrokerSalariesView(APIView):
    permission_classes = [IsAdminOrBroker]

    def get(self, request):
        company_id = request.query_params.get("company_id")
        company_name = request.query_params.get("company_name")
        if not company_id and not company_name:
            return Response(
                {"detail": "company_id or company_name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start_raw = request.query_params.get("start")
        end_raw = request.query_params.get("end")
        start_date = parse_date(start_raw) if start_raw else None
        end_date = parse_date(end_raw) if end_raw else None

        price_expr = ExpressionWrapper(
            F("quantity") * F("unit_price"),
            output_field=DecimalField(max_digits=24, decimal_places=2),
        )

        base_filter: Q = Q()
        if company_id:
            base_filter &= Q(batch__broker__company_id=company_id)
        if company_name:
            base_filter &= Q(batch__broker__company__name=company_name)
        if start_date:
            base_filter &= Q(batch__contract_date__gte=start_date)
        if end_date:
            base_filter &= Q(batch__contract_date__lte=end_date)

        per_broker = (
            BatchItem.objects.filter(base_filter)
            .values(
                "batch__broker_id",
                "batch__broker__commission_rate",
                "batch__broker__company__monthly_fee",
                "batch__broker__company__name",
            )
            .annotate(turnover=Sum(price_expr))
        )

        result = []
        for row in per_broker:
            turnover = row["turnover"] or Decimal("0")
            commission_rate = row["batch__broker__commission_rate"] or Decimal("0")
            monthly_fee = row["batch__broker__company__monthly_fee"] or Decimal("0")
            commission = turnover * commission_rate
            salary = commission - monthly_fee
            result.append(
                {
                    "broker_id": row["batch__broker_id"],
                    "company": row["batch__broker__company__name"],
                    "turnover": turnover,
                    "commission": commission,
                    "monthly_fee": monthly_fee,
                    "salary": salary,
                }
            )

        return Response(result)


class LatestTradesReportView(APIView):
    permission_classes = [IsAdminOrBroker]

    def get(self, request):
        product_totals = (
            BatchItem.objects.values("product_id")
            .annotate(total_quantity=Sum("quantity"))
            .order_by()
        )
        totals_map = {row["product_id"]: row["total_quantity"] for row in product_totals}

        items = (
            BatchItem.objects.select_related(
                "product",
                "product__manufacturer",
                "batch",
                "batch__broker",
                "batch__broker__company",
            )
            .order_by("product_id", "-batch__contract_date", "-batch_id")
        )

        seen: set[int] = set()
        per_product = []
        for item in items:
            if item.product_id in seen:
                continue
            seen.add(item.product_id)
            per_product.append(
                {
                    "product_id": item.product_id,
                    "product_code": item.product.code,
                    "product_name": item.product.name,
                    "manufacturer": item.product.manufacturer.name,
                    "last_batch_number": item.batch.number,
                    "last_batch_date": item.batch.contract_date,
                    "last_batch_quantity": item.quantity,
                    "offered_by_company": item.batch.broker.company.name,
                    "total_quantity": totals_map.get(item.product_id, Decimal("0")),
                }
            )

        total_products = len(per_product)
        total_quantity = sum((row["total_quantity"] or Decimal("0")) for row in per_product)

        return Response(
            {
                "total_products": total_products,
                "total_quantity": total_quantity,
                "items": per_product,
            }
        )

