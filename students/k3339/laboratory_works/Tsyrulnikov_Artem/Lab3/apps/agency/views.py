from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Client, Employee, Order, PaymentOrder, Service, ServiceCategory
from .serializers import (
    ClientSerializer,
    EmployeeSerializer,
    OrderSerializer,
    PaymentOrderSerializer,
    ServiceCategorySerializer,
    ServiceSerializer,
)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def orders(self, request, pk=None):
        """Список заявок заказчика за период"""
        client = self.get_object()
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        orders = Order.objects.filter(client=client)
        if date_from:
            orders = orders.filter(created_at__date__gte=date_from)
        if date_to:
            orders = orders.filter(created_at__date__lte=date_to)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def workload(self, request):
        """Список сотрудников с количеством заявок за период"""
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        employees = Employee.objects.all()
        result = []

        for emp in employees:
            orders = Order.objects.filter(executor=emp)
            if date_from:
                orders = orders.filter(created_at__date__gte=date_from)
            if date_to:
                orders = orders.filter(created_at__date__lte=date_to)

            result.append(
                {
                    "executor_name": f"{emp.last_name} {emp.first_name}",
                    "order_count": orders.count(),
                }
            )

        return Response(result)


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticated]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        """Номенклатура услуг по видам"""
        category_id = request.query_params.get("category")
        services = Service.objects.all()

        if category_id:
            services = services.filter(category_id=category_id)

        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class PaymentOrderViewSet(viewsets.ModelViewSet):
    queryset = PaymentOrder.objects.all()
    serializer_class = PaymentOrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def completed_works(self, request):
        """Список выполненных работ (оплаченных)"""
        payments = PaymentOrder.objects.filter(is_paid=True).select_related(
            "order__client", "order__service", "order__executor"
        )

        result = []
        for p in payments:
            result.append(
                {
                    "payment_date": p.payment_date,
                    "client_name": p.order.client.name,
                    "service_code": p.order.service.id,
                    "executor_name": f"{p.order.executor.last_name} {p.order.executor.first_name}",
                }
            )

        return Response(result)

    @action(detail=False, methods=["get"])
    def by_period(self, request):
        """Платежные поручения за период"""
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        payments = PaymentOrder.objects.all().select_related(
            "order__client", "order__service"
        )

        if date_from:
            payments = payments.filter(issued_date__gte=date_from)
        if date_to:
            payments = payments.filter(issued_date__lte=date_to)

        result = []
        for p in payments:
            result.append(
                {
                    "id": p.id,
                    "client_name": p.order.client.name,
                    "service_name": p.order.service.name,
                    "is_paid": p.is_paid,
                    "issued_date": p.issued_date,
                }
            )

        return Response(result)

    @action(detail=False, methods=["get"])
    def quarter_report(self, request):
        """Отчет за последний квартал"""
        quarter_ago = timezone.now().date() - timedelta(days=90)

        payments = PaymentOrder.objects.filter(
            is_paid=True, payment_date__gte=quarter_ago
        ).select_related("order__executor")

        # Группировка по исполнителям
        report = {}
        for p in payments:
            executor_name = (
                f"{p.order.executor.last_name} {p.order.executor.first_name}"
            )
            if executor_name not in report:
                report[executor_name] = 0
            report[executor_name] += float(p.order.total_cost)

        result = [{"executor_name": k, "total_cost": v} for k, v in report.items()]

        return Response(result)
