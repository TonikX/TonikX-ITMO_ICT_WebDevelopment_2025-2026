from rest_framework import serializers
from .models import Client, Employee, ServiceCategory, Service, Order, PaymentOrder


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Service
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.name", read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)
    executor_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_executor_name(self, obj):
        return f"{obj.executor.last_name} {obj.executor.first_name}"


class PaymentOrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="order.id", read_only=True)
    client_name = serializers.CharField(source="order.client.name", read_only=True)
    service_name = serializers.CharField(source="order.service.name", read_only=True)

    class Meta:
        model = PaymentOrder
        fields = "__all__"


# Сериализаторы для отчетов
class CompletedWorkSerializer(serializers.Serializer):
    """Список выполненных работ"""

    payment_date = serializers.DateField()
    client_name = serializers.CharField()
    service_code = serializers.IntegerField()
    executor_name = serializers.CharField()


class EmployeeWorkloadSerializer(serializers.Serializer):
    """Количество заявок по сотрудникам"""

    executor_name = serializers.CharField()
    order_count = serializers.IntegerField()


class QuarterReportSerializer(serializers.Serializer):
    """Отчет за квартал"""

    executor_name = serializers.CharField()
    total_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
