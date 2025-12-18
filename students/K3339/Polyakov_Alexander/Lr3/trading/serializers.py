from rest_framework import serializers

from .models import Batch, BatchItem, Broker, BrokerCompany, Manufacturer, Product


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BrokerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerCompany
        fields = "__all__"


class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = "__all__"


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"


class BatchItemSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = BatchItem
        fields = "__all__"

    def get_is_expired(self, obj: BatchItem) -> bool:
        return obj.is_expired

    def get_total_price(self, obj: BatchItem):
        return obj.total_price

